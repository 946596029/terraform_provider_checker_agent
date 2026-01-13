"""FastAPI server exposing the translation chain."""

from fastapi import FastAPI
from langserve import add_routes
import uvicorn

from ..chains import translation_chain
from ..config import settings

app = FastAPI(
    title="LangChain Translation Server",
    version="1.0.0",
    description="A simple API server using LangChain's Runnable interfaces.",
)

# Add the LCEL chain as a REST endpoint at /chain.
add_routes(app, translation_chain, path="/chain")


def run() -> None:
    """Launch the FastAPI app with uvicorn."""

    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    run()