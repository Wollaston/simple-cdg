import asyncio
from itertools import chain
from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from starlette.status import HTTP_204_NO_CONTENT

from app.models import BillBase, BillPublic, ChunkPublic, IdQuery, TextQuery
from app.state import State, get_state

RESOURCE: str = "bill"

router = APIRouter(
    prefix="/bills",
    tags=["bills"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{congress}/{bill_type}")
async def list_bills(
    *,
    state: Annotated[State, Depends(get_state)],
    congress: int,
    bill_type: Literal["hr", "s", "hjres", "sjres", "hconres", "sres"],
    offset: int,
    limit: int,
) -> list[BillPublic]:
    base_bills = [
        BillBase.model_validate(data)
        for data in state.client.client.get(
            f"/{RESOURCE}/{congress}/{bill_type}{state.client.format(offset=offset, limit=limit)}"
        ).json()["bills"]
    ]

    bills = await state.client.get_bill_text(bills=base_bills)

    texts_chunks = await asyncio.gather(
        *[state.chunker.chunk(bill=bill) for bill in bills]
    )

    embedded_chunks = await asyncio.gather(
        *[
            state.embedder.embed_chunks(cdg_id=bill.cdg_id, chunks=chunks)
            for bill, chunks in zip(bills, texts_chunks)
        ]
    )

    opensearch_ids = await asyncio.gather(
        *[state.opensearch.add(chunks=chunks) for chunks in chain(embedded_chunks)],
    )
    for chunk_list, id_list in zip(embedded_chunks, opensearch_ids):
        for chunk, id in zip(chunk_list, id_list):
            chunk.chunk.opensearch_id = id

    await asyncio.gather(
        *[state.db.insert_chunks(chunks=chunks) for chunks in chain(embedded_chunks)],
    )

    return await state.db.insert_bills(bills=bills)


@router.post("/detail")
async def bill_detail(
    id: IdQuery,
    *,
    state: Annotated[State, Depends(get_state)],
) -> BillPublic | int:
    bill = await state.db.get_bill_by_id(bill_id=id.id)
    if bill:
        return bill
    else:
        return HTTP_204_NO_CONTENT


@router.post("/search/bills/{k}")
async def bill_search(
    text: TextQuery,
    *,
    state: Annotated[State, Depends(get_state)],
    k: int,
) -> list[BillPublic]:
    embedding = await state.embedder.embed_query(text.text)
    results = state.opensearch.search(embedding=embedding, k=k)
    chunks = await state.db.get_bills_by_ids(bill_ids=[bill.cdg_id for bill in results])
    return chunks


@router.post("/search/{k}")
async def chunk_search(
    text: TextQuery,
    *,
    state: Annotated[State, Depends(get_state)],
    k: int,
) -> list[ChunkPublic]:
    embedding = await state.embedder.embed_query(text.text)
    results = state.opensearch.search(embedding=embedding, k=k)
    chunks = await state.db.get_chunks_by_ids(chunk_ids=[chunk.id for chunk in results])
    return chunks


@router.get("/list")
async def all_bills(
    *,
    state: Annotated[State, Depends(get_state)],
) -> list[BillPublic]:
    return await state.db.get_bills()
