import asyncio
import os

from httpx import AsyncClient, Response
from httpx import Client as HttpxClient

from app.models import BillBase, BillCreate, TextVersions


class Client:
    key: str
    client: HttpxClient
    base_url: str
    timeout: int

    def __init__(self, *, base_url: str, key: str, timeout: int = 120):
        self.key = key
        self.client = HttpxClient(base_url=base_url, timeout=timeout)
        self.base_url = base_url
        self.timeout = timeout

    @classmethod
    def from_env(cls) -> "Client":
        host: str = os.getenv("CDG_HOST", "https://api.congress.gov")
        server: str = os.getenv("CDG_VERSION", "v3")
        key: str = os.getenv("CDG_KEY", "TQTJZbdc9lJr1UIFewWKJXlDqSIW1u6uToJWT3DC")
        timeout: int = int(os.getenv("HTTP_TIMEOUT", 120))

        return Client(base_url=f"{host}/{server}", key=key, timeout=timeout)

    def get(self, url: str) -> Response:
        return self.client.get(url)

    def format(self, **kwargs) -> str:
        params: list[str] = []
        for key, value in kwargs.items():
            params.append(f"{key}={value}")
        return f"?format=json&api_key={self.key}&{'&'.join(params)}"

    async def get_bill_text(
        self,
        *,
        bills: list[BillBase],
    ) -> list[BillCreate]:
        NOISE: dict[str, str] = {
            "<html><body><pre>": "",
            "</pre></body></html>": "",
            "&lt;DOC&gt;": "",
            "&lt;all&gt;": "",
            "_": "",
        }

        bills_create: list[BillCreate] = []
        async with AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            url_responses = await asyncio.gather(
                *[
                    client.get(
                        f"/bill/{bill.congress}/{bill.type.lower()}/{bill.number}/text{self.format()}"
                    )
                    for bill in bills
                ]
            )

            urls: list[str] = []
            for response in url_responses:
                url = (
                    [
                        TextVersions.model_validate(data)
                        for data in response.json()["textVersions"]
                    ][0]
                    .formats[0]  # ty: ignore
                    .url
                )
                urls.append(url)

            text_responses = await asyncio.gather(*[client.get(url) for url in urls])

            for bill, response in zip(bills, text_responses):
                raw_text = response.text
                text = " ".join(raw_text.split())

                for val in NOISE:
                    text = text.replace(val, "")

                bills_create.append(
                    BillCreate.from_base(
                        base=bill, text=text, raw_text=raw_text, chunks=[]
                    )
                )

        return bills_create
