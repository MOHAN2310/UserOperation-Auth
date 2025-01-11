from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["HealthOperation"]
)


@router.get("/")
def health_check():
    return {"status": "ok"}