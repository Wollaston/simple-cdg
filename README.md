# Simple CDG

A simple application for information retrieval of data on [congress.gov](https://api.congress.gov).

## Structure

This app uses `docker compose` to network several services together. Without refactoring,
this project needs to be run with `docker compose` so that it is OS and architecture
agnostic, and so the networking environment works as the services all communicate
over the network using the service names. It also prevents any use from having
to download dependencies, such as `node`.

## Services

There are several services composed. Here is a quick summary:

- `init` initializes the data environment on the local computer for
`postgres` and `opensearch`
- `sveltekit` is the fullstack frontend web app using the `sveltekit` framework
- `fastapi` is a backend `fastapi` app for retrieving congressional data
from `api.congress.gov`, embedding it, and storing it in the `postgres`
for `sveltekit` to use and render to views.
- `postgres` is a `postgres` database configure for storing congressional
bills and their respective embedded chunks (set to 128 tokens, with overlap
of 16 tokens) relations for `sveltekit` retrieval and rendering to views.
- `vllm` is the inference engine that hosts the embedding model
`sentence-transformers/all-MiniLM-L6-v2`
- `opensearch` is an open-source `elasticsearch` for that stores the chunk
embeddings for `knn` retrieval (k=10).
- `opensearch-dashboard` is a utility dashboard for interacting with
`opensearch`, with the intention of making local development easier.

## Running the Services

To run the services, simply `docker compose up`.

## Interacting with the Services

After running the services, navigate to `http://localhost:3000`
for the frontend interface. The rest of the up is interactive
and self-explanatory. The other services are not intended
to be accessed directly by the end-user.
