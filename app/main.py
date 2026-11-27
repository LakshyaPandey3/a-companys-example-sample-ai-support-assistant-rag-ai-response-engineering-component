from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="AI Support Assistant API",
    description=(
        "A retrieval-augmented generation (RAG) service "
        "for evidence-based question answering."
    ),
    version="1.0.0",
)

app.include_router(router)
