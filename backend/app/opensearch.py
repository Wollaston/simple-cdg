import os

from opensearchpy import OpenSearch as OpenSearchClient
from opensearchpy import helpers

from app.models import EmbeddedChunk, SearchResult


class OpenSearch:
    client: OpenSearchClient

    def __init__(
        self,
        host: str,
        port: int,
        index_name: str,
        dimensions: int,
    ):
        self.index_name = index_name
        self.client = OpenSearchClient(
            hosts=[{"host": host, "port": port}],
            http_compress=True,  # enables gzip compression for request bodies
            use_ssl=False,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )
        self._init_index(dimensions=dimensions)

    @classmethod
    def from_env(cls) -> "OpenSearch":
        host: str = os.getenv("OPENSEARCH_HOST", "localhost")
        port: int = int(os.getenv("OPENSEARCH_PORT", 9200))
        index_name: str = os.getenv("OPENSEARCH_INDEX", "cdg")
        dimensions: int = int(os.getenv("OPENSEARCH_DIMENSIONS", 384))

        return OpenSearch(
            host=host,
            port=port,
            index_name=index_name,
            dimensions=dimensions,
        )

    async def add(self, *, chunks: list[EmbeddedChunk]) -> list[str]:
        responses = [
            res
            for _, res in helpers.streaming_bulk(
                self.client,
                [
                    self._format(cdg_id=chunk.chunk.cdg_id, embedding=chunk.embedding)
                    for chunk in chunks
                ],
            )
        ]
        self.client.indices.refresh(index=self.index_name)
        return [res["index"]["_id"] for res in responses]

    def search(
        self, *, embedding: list[float | int], k: int = 10
    ) -> list[SearchResult]:
        query = {
            "size": k,
            "query": {"knn": {"embedding": {"vector": embedding, "k": k}}},
        }
        results = self.client.search(index=self.index_name, body=query)
        return [
            SearchResult(id=hit["_id"], cdg_id=hit["_source"]["cdg_id"])
            for hit in results["hits"]["hits"]
        ]

    def _format(
        self, *, cdg_id: str, embedding: list[int | float]
    ) -> dict[str, str | list[float]]:
        return {
            "_index": self.index_name,
            "cdg_id": cdg_id,
            "embedding": embedding,
        }

    def _init_index(self, *, dimensions: int) -> None:
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(
                index=self.index_name,
                body={
                    "settings": {
                        "index": {
                            "knn": True,
                            "number_of_shards": 1,
                            "number_of_replicas": 0,
                        },
                    },
                    "mappings": {
                        "properties": {
                            "embedding": {
                                "type": "knn_vector",
                                "dimension": dimensions,
                            },
                            "cdg_id": {"type": "text"},
                        }
                    },
                },
            )
