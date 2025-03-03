from constants import messages
from fastapi import APIRouter

# /status Endpoint
router = APIRouter()
@router.get("/api/status")
def status():
    return {
        "status": "success",
        "message": messages.statusMessage,
    }
