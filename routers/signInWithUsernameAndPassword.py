from asyncpg import Connection
from constants import strings
from fastapi import APIRouter, Depends, HTTPException
from helpers.databaseHelper import getDatabaseConnection
from passlib.context import CryptContext
from pydantic import BaseModel

# Request Model
class SignInRequest(BaseModel):
    username: str
    password: str

# /signInWithUsernameAndPassword Endpoint
router = APIRouter()
@router.post("/api/signInWithUsernameAndPassword")
async def signInWithUsernameAndPassword(
    request: SignInRequest,
    db: Connection = Depends(getDatabaseConnection)
):
    try:
        if request.username is None:
            raise HTTPException(status_code=400, detail=strings.usernameRequiredMessage)

        if request.password is None:
            raise HTTPException(status_code=400, detail=strings.passwordRequiredMessage)
    
        query = "SELECT * FROM users WHERE username = $1"
        user = await db.fetchrow(query, request.username)

        if not user:
            raise HTTPException(status_code=404, detail=strings.userNotFoundErrorMessage)

        cryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        if not cryptContext.verify(request.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail=strings.wrongPasswordErrorMessage)

        return {
            "status": "success",
            "message": "Sign in successful.",
            "user": {
                "id": user["id"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "email_address": user["email_address"],
                "username": user["username"],
                "about": user["about"],
                "image_path": user["image_path"],
                "created_at": user["created_at"],
                "updated_at": user["updated_at"],
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception on signInWithUsernameAndPassword: {e}")
        raise HTTPException(status_code=500, detail=strings.serverErrorMessage)
    finally:
        await db.close()
