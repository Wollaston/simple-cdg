import os

from chonkie import TokenChunker
from transformers import AutoTokenizer

from app.models import BillCreate


class Chunker:
    chunker: TokenChunker

    def __init__(
        self,
        *,
        model: str,
        chunk_size: int,
        chunk_overlap: int,
    ):
        self.model = model
        tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.chunker = TokenChunker(
            tokenizer=tokenizer,  # ty: ignore
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    @classmethod
    def from_env(cls) -> "Chunker":
        model: str = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        chunk_size: int = int(os.getenv("EMBED_CHUNK_SIZE", 128))
        chunk_overlap: int = int(os.getenv("EMBED_CHUNK_OVERLAP", 16))

        return Chunker(model=model, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    async def chunk(self, *, bill: BillCreate) -> list[str]:
        return [chunk.text for chunk in self.chunker.chunk(text=bill.text)]
