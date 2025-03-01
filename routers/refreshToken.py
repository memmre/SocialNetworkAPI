from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException
from helpers.authentication import ALGORITHM, REFRESH_SECRET_KEY, create_access_token
from helpers.databaseHelper import getDatabaseConnection
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel

# Request Model
class RefreshTokenRequest(BaseModel):
    refresh_token: str

# /refreshToken Endpoint
router = APIRouter()
@router.post("/api/refreshToken")
async def refresh_access_token(request: RefreshTokenRequest, db: Connection = Depends(getDatabaseConnection)):
    try:
        query = "SELECT email_address FROM users WHERE refresh_token = $1"
        user = await db.fetchrow(query, request.refresh_token)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        try:
            payload = decode(request.refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
            email_address = payload.get("sub")

            if email_address != user["email_address"]:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")

        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        access_token = create_access_token(data={"sub": email_address})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception on refresh_access_token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    