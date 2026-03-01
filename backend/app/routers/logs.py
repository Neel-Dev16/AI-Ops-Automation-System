from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def list_logs() -> dict[str, str]:
    return {"message": "Logs endpoint placeholder."}
