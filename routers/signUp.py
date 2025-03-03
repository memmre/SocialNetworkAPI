from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException
from constants import errorMessages, messages
from helpers.authentication import cryptContext, createAccessToken, createRefreshToken
from helpers.databaseHelper import getDatabaseConnection
from models.signUpRequest import SignUpRequest

# /signUp Endpoint
router = APIRouter()
@router.post("/api/signUp")
async def signUp(
    request: SignUpRequest,
    database: Connection = Depends(getDatabaseConnection)
):
    try:
        if not request.firstName:
            raise HTTPException(status_code=400, detail=errorMessages.firstNameRequiredMessage)
        if not request.lastName:
            raise HTTPException(status_code=400, detail=errorMessages.lastNameRequiredMessage)
        if not request.emailAddress:
            raise HTTPException(status_code=400, detail=errorMessages.emailAddressRequiredMessage)
        if not request.username:
            raise HTTPException(status_code=400, detail=errorMessages.usernameRequiredMessage)
        if not request.password:
            raise HTTPException(status_code=400, detail=errorMessages.passwordRequiredMessage)
        
        # Check Email Address Availability
        checkEmailAddressQuery = "SELECT id FROM users WHERE email_address = $1"
        emailAddressMatchedUser = await database.fetchrow(checkEmailAddressQuery, request.emailAddress)
        
        if emailAddressMatchedUser:
            raise HTTPException(status_code=400, detail=errorMessages.emailAddressInUseMessage)
        
        # Check Username Availability
        checkUsernameQuery = "SELECT id FROM users WHERE username = $1"
        usernameMatchedUser = await database.fetchrow(checkUsernameQuery, request.username)
        
        if usernameMatchedUser:
            raise HTTPException(status_code=400, detail=errorMessages.usernameInUseMessage)
        
        # Hash Password
        hashedPassword = cryptContext.hash(request.password)
        
        # Create New User
        createUserQuery = """
            INSERT INTO users (first_name, last_name, email_address, username, password_hash)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, first_name, last_name, email_address, username, about, image_path, created_at, updated_at
        """
        user = await database.fetchrow(
            createUserQuery,
            request.firstName, request.lastName, request.emailAddress, request.username, hashedPassword,
        )
        
        # Generate tokens
        accessToken = createAccessToken(data={"sub": user["email_address"]})
        refreshToken = createRefreshToken(data={"sub": user["email_address"]})
        
        # Update the refresh token in database
        updateTokenQuery = "UPDATE users SET refresh_token = $1 WHERE email_address = $2"
        await database.execute(updateTokenQuery, refreshToken, request.emailAddress)
        
        return {
            "status": "success",
            "message": messages.signUpSuccessMessage,
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
        print(f"Exception on signUp: {e}")
        raise HTTPException(status_code=500, detail=errorMessages.serverErrorMessage)
