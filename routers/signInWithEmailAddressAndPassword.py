from asyncpg import Connection
from constants import strings
from fastapi import APIRouter, Depends, HTTPException
from helpers.databaseHelper import getDatabaseConnection
from passlib.context import CryptContext
from pydantic import BaseModel

# Request Model
class SignInRequest(BaseModel):
    email_address: str
    password: str

# /signInWithEmailAddressAndPassword Endpoint
router = APIRouter()
@router.post("/api/signInWithEmailAddressAndPassword")
async def signInWithEmailAddressAndPassword(
    request: SignInRequest,
    db: Connection = Depends(getDatabaseConnection)
):
    try:
        if request.email_address is None:
            raise HTTPException(status_code=400, detail=strings.emailAddressRequiredMessage)

        if request.password is None:
            raise HTTPException(status_code=400, detail=strings.passwordRequiredMessage)
    
        query = "SELECT * FROM users WHERE email_address = $1"
        user = await db.fetchrow(query, request.email_address)

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
        print(f"Exception on signInWithEmailAddressAndPassword: {e}")
        raise HTTPException(status_code=500, detail=strings.serverErrorMessage)
    finally:
        await db.close()
