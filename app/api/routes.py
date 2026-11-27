from fastapi import APIRouter

from app.api.schemas import HealthResponse


router = APIRouter(
    prefix="/api/v1",
    tags=["Health"],
)


@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health_check() -> HealthResponse:
    """Check whether the API service is responding."""
    return HealthResponse(status="healthy")
