import os

from sqlmodel import Session, SQLModel, create_engine

from app.models import Bill, BillPublic


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
        host: str = os.getenv("DB_HOUST", "localhost")
        port: int = int(os.getenv("DB_PORT", 5432))
        dbname: str = os.getenv("DB_DBNAME", "cdg")

        return Db(
            user=user,
            password=password,
            host=host,
            port=port,
            dbname=dbname,
        )

    async def insert_bills(self, *, bills: list[Bill]) -> list[BillPublic]:
        with Session(self.engine) as session:
            session.add_all(bills)
            session.commit()
            [session.refresh(bill) for bill in bills]

        return [BillPublic.model_validate(bill) for bill in bills]

    def _get_session(self) -> Session:  # ty: ignore
        with Session(self.engine) as session:
            yield session

    def _create_db_and_tables(self) -> None:
        SQLModel.metadata.create_all(self.engine)
