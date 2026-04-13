import asyncio
import os

from chonkie import TokenChunker
from openai import AsyncOpenAI
from tokenizers import Tokenizer


class Embedder:
    model: str
    client: AsyncOpenAI
    chunker: TokenChunker

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model: str,
        chunk_size: int,
        chunk_overlap: int,
    ):
        self.model = model
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.chunker = self._get_chunker(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    @classmethod
    def from_env(cls) -> "Embedder":
        base_url: str = os.getenv("EMBED_URL", "http://localhost:8888/v1")
        api_key: str = os.getenv("EMBED_API_KEY", "LOCAL")
        model: str = os.getenv("EMBED_MODEL", "Qwen/Qwen3-Embedding-0.6B")
        chunk_size: int = int(os.getenv("EMBED_CHUNK_SUZE", 128))
        chunk_overlap: int = int(os.getenv("EMBED_CHUNK_OVERLAP", 16))

        return Embedder(
            base_url=base_url,
            api_key=api_key,
            model=model,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    async def embed(self, text: str) -> list[dict[str, str | list[float | int]]]:
        chunks = [chunk.text for chunk in self.chunker.chunk(text)]
        responses = await self.client.embeddings.create(
            input=chunks,
            model=self.model,
        )

        return [
            {"text": text, "embedding": embedding.embedding}
            for text, embedding in zip(chunks, responses.data)
        ]

    def _get_chunker(self, *, chunk_size: int, chunk_overlap: int) -> TokenChunker:
        tokenizer = Tokenizer.from_pretrained(self.model)

        return TokenChunker(
            tokenizer=tokenizer, chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
