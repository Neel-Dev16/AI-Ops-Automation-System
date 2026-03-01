from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def list_incidents() -> dict[str, str]:
    return {"message": "Incidents endpoint placeholder."}
