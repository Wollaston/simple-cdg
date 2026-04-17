import os

from openai import AsyncOpenAI

from app.models import ChunkBase, EmbeddedChunk


class Embedder:
    model: str
    client: AsyncOpenAI

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model: str,
    ):
        self.model = model
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    @classmethod
    def from_env(cls) -> "Embedder":
        base_url: str = os.getenv("EMBED_URL", "http://localhost:8888/v1")
        api_key: str = os.getenv("EMBED_API_KEY", "LOCAL")
        model: str = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

        return Embedder(
            base_url=base_url,
            api_key=api_key,
            model=model,
        )

    async def embed_query(self, query: str) -> list[float | int]:
        responses = await self.client.embeddings.create(
            input=query,
            model=self.model,
        )

        return responses.data[0].embedding

    async def embed_chunks(self, cdg_id: str, chunks: list[str]) -> list[EmbeddedChunk]:
        responses = await self.client.embeddings.create(
            input=chunks,
            model=self.model,
        )

        return [
            EmbeddedChunk(
                chunk=ChunkBase(text=chunk, cdg_id=cdg_id),
                embedding=embedding.embedding,
            )
            for chunk, embedding in zip(chunks, responses.data)
        ]
