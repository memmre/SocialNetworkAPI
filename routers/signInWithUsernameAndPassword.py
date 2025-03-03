from asyncpg import Connection
from constants import errorMessages, messages
from fastapi import APIRouter, Depends, HTTPException
from helpers.authentication import cryptContext, createAccessToken, createRefreshToken
from helpers.databaseHelper import getDatabaseConnection
from models.signInRequest import SignInRequest

# /signInWithUsernameAndPassword Endpoint
router = APIRouter()
@router.post("/api/signInWithUsernameAndPassword")
async def signInWithUsernameAndPassword(
    request: SignInRequest,
    database: Connection = Depends(getDatabaseConnection)
):
    try:
        if not request.identifier:
            raise HTTPException(status_code=400, detail=errorMessages.usernameRequiredMessage)
        if not request.password:
            raise HTTPException(status_code=400, detail=errorMessages.passwordRequiredMessage)
    
        getUserQuery = """
            SELECT id, first_name, last_name, email_address, username, password_hash, about, image_path, created_at, updated_at
            FROM users WHERE username = $1
        """
        user = await database.fetchrow(getUserQuery, request.identifier)

        if not user:
            raise HTTPException(status_code=404, detail=errorMessages.userNotFoundMessage)
        
        if not cryptContext.verify(request.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail=errorMessages.wrongPasswordMessage)

        # Generate tokens
        accessToken = createAccessToken(data={"sub": user["email_address"]})
        refreshToken = createRefreshToken(data={"sub": user["email_address"]})

        # Update the refresh token in database
        updateTokenQuery = "UPDATE users SET refresh_token = $1 WHERE username = $2"
        await database.execute(updateTokenQuery, refreshToken, request.identifier)
        
        return {
            "status": "success",
            "message": messages.signInSuccessMessage,
            "accessToken": accessToken,
            "refreshToken": refreshToken,
            "tokenType": "bearer",
            "user": {
                "id": user["id"],
                "firstName": user["first_name"],
                "lastName": user["last_name"],
                "emailAddress": user["email_address"],
                "username": user["username"],
                "about": user["about"],
                "imagePath": user["image_path"],
                "createdAt": user["created_at"],
                "updatedAt": user["updated_at"],
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception on signInWithUsernameAndPassword: {e}")
        raise HTTPException(status_code=500, detail=errorMessages.serverErrorMessage)
