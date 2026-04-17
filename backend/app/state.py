from dataclasses import dataclass

from fastapi import Request

from app.chunker import Chunker
from app.client import Client
from app.db import Db
from app.embedding import Embedder
from app.opensearch import OpenSearch


@dataclass
class State:
    db: Db
    embedder: Embedder
    opensearch: OpenSearch
    client: Client
    chunker: Chunker

    @classmethod
    def from_env(cls) -> "State":
        return State(
            db=Db.from_env(),
            embedder=Embedder.from_env(),
            opensearch=OpenSearch.from_env(),
            client=Client.from_env(),
            chunker=Chunker.from_env(),
        )


def get_state(request: Request) -> State:
    return request.app.state.state
