from constants import strings
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": strings.rootMessage}
