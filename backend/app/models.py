from dataclasses import dataclass

from pydantic import BaseModel
from pydantic import Field as PydanticField
from sqlmodel import Field, Relationship, SQLModel


class Formats(BaseModel):
    type: str | None = PydanticField(None, examples=["Formatted Text"])
    url: str


class TextVersions(BaseModel):
    formats: list[Formats] | None = None
    type: str | None = PydanticField(None, examples=["Enrolled Bill"])


@dataclass
class SearchResult:
    id: str
    cdg_id: str


class TextQuery(BaseModel):
    text: str


class IdQuery(BaseModel):
    id: str


class BillBase(SQLModel):
    congress: int
    number: int
    originChamber: str
    originChamberCode: str
    title: str
    type: str
    cdg_id: str = Field(
        default_factory=lambda data: (  # ty: ignore
            f"{data['congress']}_{data['type']}_{data['number']}"
        ),
        index=True,
    )


class Bill(BillBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    raw_text: str
    text: str

    chunks: list["Chunk"] = Relationship(back_populates="bill")


class BillCreate(BillBase):
    raw_text: str
    text: str

    chunks: list["Chunk"]

    @classmethod
    def from_base(
        cls, *, base: BillBase, text: str, raw_text: str, chunks: list["Chunk"]
    ) -> "BillCreate":
        return BillCreate(
            congress=base.congress,
            number=base.number,
            originChamber=base.originChamber,
            originChamberCode=base.originChamberCode,
            title=base.title,
            type=base.type,
            cdg_id=base.cdg_id,
            text=text,
            raw_text=raw_text,
            chunks=chunks,
        )


class BillPublic(BillBase):
    id: int
    raw_text: str
    text: str


class ChunkBase(SQLModel):
    text: str
    opensearch_id: str | None = Field(default=None, index=True)
    cdg_id: str = Field(index=True)

    bill_id: int | None = Field(default=None, foreign_key="bill.id")


class Chunk(ChunkBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    bill: Bill | None = Relationship(back_populates="chunks")


class ChunkCreate(ChunkBase):
    pass


class ChunkPublic(ChunkBase):
    id: int


class ChunkPublicWithBill(ChunkPublic):
    bill: Bill


@dataclass
class EmbeddedChunk:
    chunk: ChunkBase
    embedding: list[int | float]
