import asyncio
from typing import Annotated, Literal

from fastapi import APIRouter, Depends

from app.models import Bill, BillPublic, TextQuery
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
    bills = [
        Bill.model_validate(data)
        for data in state.client.get(
            f"/{RESOURCE}/{congress}/{bill_type}/{state.client.format(offset=offset, limit=limit)}"
        ).json()["bills"]
    ]

    texts = await asyncio.gather(
        *[
            state.client.get_bill_text(
                congress=congress,
                bill_type=bill_type,
                bill_number=bill.number,
                offset=offset,
                limit=limit,
            )
            for bill in bills
        ]
    )
    embeddings = await asyncio.gather(
        *[state.embedder.embed(text.text) for text in texts]
    )
    asyncio.gather(
        *[
            state.opensearch.add(embeddings=[embedding for embedding in group])
            for group in embeddings
        ]
    )

    return await state.db.insert_bills(bills=bills)


@router.post("/search/{k}")
async def bill_search(
    text: TextQuery,
    *,
    state: Annotated[State, Depends(get_state)],
    k: int,
) -> list[dict[str, str]]:
    embedding = (await state.embedder.embed(text.text))[0]
    res = state.opensearch.search(embedding=embedding["embedding"], k=k)
    return res
