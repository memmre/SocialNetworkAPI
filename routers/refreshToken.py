from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException
from constants import exceptionMessages
from helpers.authentication import ALGORITHM, REFRESH_SECRET_KEY, createAccessToken
from helpers.databaseHelper import getDatabaseConnection
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from models.refreshTokenRequest import RefreshTokenRequest

# /refreshToken Endpoint
router = APIRouter()
@router.post("/api/refreshToken")
async def refreshToken(
    request: RefreshTokenRequest,
    database: Connection = Depends(getDatabaseConnection),
):
    try:
        if not request.refreshToken:
            raise HTTPException(status_code=400, detail=exceptionMessages.refreshTokenRequiredMessage)
        
        query = "SELECT email_address FROM users WHERE refresh_token = $1"
        user = await database.fetchrow(query, request.refreshToken)
        
        if not user:
            raise HTTPException(status_code=401, detail=exceptionMessages.invalidRefreshTokenMessage)

        try:
            payload = decode(request.refreshToken, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
            emailAddress = payload.get("sub")

            if emailAddress != user["email_address"]:
                raise HTTPException(status_code=401, detail=exceptionMessages.invalidRefreshTokenMessage)

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail=exceptionMessages.expiredRefreshTokenMessage)
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail=exceptionMessages.invalidRefreshTokenMessage)

        accessToken = createAccessToken(data={"sub": emailAddress})

        return {
            "accessToken": accessToken,
            "tokenType": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception on refreshToken: {e}")
        raise HTTPException(status_code=500, detail=exceptionMessages.serverErrorMessage)
