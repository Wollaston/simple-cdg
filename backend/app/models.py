from pydantic import BaseModel
from pydantic import Field as PydanticField
from sqlmodel import Field, SQLModel


class TextQuery(BaseModel):
    text: str


class Text(BaseModel):
    raw_text: str
    text: str


class BillBase(SQLModel):
    congress: int
    number: str
    originChamber: str
    originChamberCode: str
    title: str
    type: str
    raw_text: str | None = Field(None)
    text: str | None = Field(None)
    embedded: bool = Field(False)
    cdg_id: str = Field(  # ty: ignore
        default_factory=lambda data: (
            f"{data['congress']}_{data['type']}_{data['number']}"
        )
    )


class Bill(BillBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BillCreate(BillBase):
    pass


class BillPublic(BillBase):
    id: int


class SponsorBase(SQLModel):
    bioguideId: str = Field(index=True)
    firstName: str
    lastName: str
    fullName: str
    isByRequest: str
    middleName: str
    party: str
    state: str


class Sponsor(SponsorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class SponsorCreate(SponsorBase):
    pass


class SponsorPublic(SponsorBase):
    id: str


class Formats(BaseModel):
    type: str | None = PydanticField(None, examples=["Formatted Text"])
    url: str


class TextVersions(BaseModel):
    formats: list[Formats] | None = None
    type: str | None = PydanticField(None, examples=["Enrolled Bill"])
