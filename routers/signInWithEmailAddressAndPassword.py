from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException
from helpers.authentication import cryptContext, create_access_token, create_refresh_token
from helpers.databaseHelper import getDatabaseConnection
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
        if not request.email_address:
            raise HTTPException(status_code=400, detail="Email address is required")
        if not request.password:
            raise HTTPException(status_code=400, detail="Password is required")
    
        query = """
            SELECT id, first_name, last_name, email_address, username, about, image_path, created_at, updated_at, password_hash 
            FROM users WHERE email_address = $1
        """
        user = await db.fetchrow(query, request.email_address)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not cryptContext.verify(request.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Wrong password")

        access_token = create_access_token(data={"sub": user["email_address"]})
        refresh_token = create_refresh_token(data={"sub": user["email_address"]})

        await db.execute("UPDATE users SET refresh_token = $1 WHERE email_address = $2", refresh_token, request.email_address)

        return {
            "status": "success",
            "message": "Sign in successful.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
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
        raise HTTPException(status_code=500, detail="Internal server error")
