import os

from httpx import AsyncClient as HttpxClient

from app.models import Text, TextVersions


class Client:
    key: str
    client: HttpxClient

    def __init__(self, *, base_url: str, key: str, timeout: int = 15):
        self.key = key
        self.client = HttpxClient(base_url=base_url, timeout=timeout)

    @classmethod
    def from_env(cls) -> "Client":
        host: str = os.getenv("CDG_HOST", "https://api.congress.gov")
        server: str = os.getenv("CDG_VERSION", "v3")
        key: str = os.getenv("CDG_KEY", "TQTJZbdc9lJr1UIFewWKJXlDqSIW1u6uToJWT3DC")
        timeout: int = int(os.getenv("HTTP_TIMEOUT", 15))

        return Client(base_url=f"{host}/{server}", key=key, timeout=timeout)

    async def get(self, url: str):
        async with self.client as client:
            return await client.get(url)

    def format(self, **kwargs) -> str:
        params: list[str] = []
        for key, value in kwargs.items():
            params.append(f"{key}={value}")
        return f"?format=json&api_key={self.key}&{'&'.join(params)}"

    async def get_bill_text(
        self,
        *,
        congress: int,
        bill_type: str,
        bill_number: str,
        offset: int,
        limit: int,
    ) -> Text:
        NOISE: dict[str, str] = {
            "<html><body><pre>": "",
            "</pre></body></html>": "",
            "&lt;DOC&gt;": "",
            "&lt;all&gt;": "",
        }

        response = await self.client.get(
            f"/bill/{congress}/{bill_type}/{bill_number}/text{self.format(offset=offset, limit=limit)}"
        )

        url = (
            [
                TextVersions.model_validate(data)
                for data in response.json()["textVersions"]
            ][0]
            .formats[0]  # ty: ignore
            .url
        )
        response = await self.client.get(url)
        raw_text = response.text
        text = " ".join(raw_text.split())
        for val in NOISE:
            text = text.replace(val, "")
        return Text(raw_text=raw_text.strip(), text=text.strip())
