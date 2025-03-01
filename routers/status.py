from constants import strings
from fastapi import APIRouter

router = APIRouter()

# /status Endpoint
@router.get("/api/status")
def root():
    return {
        "status": "success",
        "message": strings.statusMessage,
    }
