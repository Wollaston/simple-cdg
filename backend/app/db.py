import os

from sqlmodel import Session, SQLModel, col, create_engine, select

from app.models import Bill, BillCreate, BillPublic, Chunk, ChunkPublic, EmbeddedChunk


class Db:
    def __init__(
        self,
        *,
        user: str,
        password: str,
        host: str,
        port: int,
        dbname: str,
    ):
        self.uri = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        self.engine = create_engine(self.uri)
        self._create_db_and_tables()

    @classmethod
    def from_env(cls) -> "Db":
        user: str = os.getenv("DB_USER", "root")
        password: str = os.getenv("DB_PASSWORD", "root")
        host: str = os.getenv("DB_HOST", "localhost")
        port: int = int(os.getenv("DB_PORT", 5432))
        dbname: str = os.getenv("DB_DBNAME", "cdg")

        return Db(
            user=user,
            password=password,
            host=host,
            port=port,
            dbname=dbname,
        )

    async def insert_bills(self, *, bills: list[BillCreate]) -> list[BillPublic]:
        with Session(self.engine) as session:
            db_bills = [Bill.model_validate(bill) for bill in bills]
            session.add_all(db_bills)
            session.commit()
            [session.refresh(bill) for bill in db_bills]

        return [BillPublic.model_validate(bill) for bill in db_bills]

    async def insert_chunks(self, *, chunks: list[EmbeddedChunk]) -> None:
        with Session(self.engine) as session:
            db_chunks = [Chunk.model_validate(chunk.chunk) for chunk in chunks]
            session.add_all(db_chunks)
            session.commit()
            [session.refresh(chunk) for chunk in db_chunks]

    async def get_bill_by_id(self, *, bill_id: str) -> BillPublic | None:
        with Session(self.engine) as session:
            statement = select(Bill).where(Bill.cdg_id == bill_id)
            bill = session.exec(statement).first()
            if bill:
                return BillPublic.model_validate(bill)
            else:
                return None

    async def get_bills(self) -> list[BillPublic]:
        with Session(self.engine) as session:
            statement = select(Bill)
            bills = session.exec(statement)
            return [BillPublic.model_validate(bill) for bill in bills]

    async def get_bills_by_ids(self, *, bill_ids: list[str]) -> list[BillPublic]:
        with Session(self.engine) as session:
            statement = select(Bill).where(col(Bill.cdg_id).in_(bill_ids))
            bills = session.exec(statement).all()
            return [BillPublic.model_validate(bill) for bill in bills]

    async def get_chunks_by_ids(self, *, chunk_ids: list[str]) -> list[ChunkPublic]:
        with Session(self.engine) as session:
            statement = select(Chunk).where(col(Chunk.opensearch_id).in_(chunk_ids))
            chunks = session.exec(statement).all()
            return [ChunkPublic.model_validate(chunk) for chunk in chunks]

    def _get_session(self) -> Session:  # ty: ignore
        with Session(self.engine) as session:
            yield session

    def _create_db_and_tables(self) -> None:
        SQLModel.metadata.create_all(self.engine)
