from fastapi import FastAPI
from routers import refreshToken, signInWithEmailAddressAndPassword, signInWithUsernameAndPassword, status

app = FastAPI()
app.include_router(status.router)
app.include_router(signInWithEmailAddressAndPassword.router)
app.include_router(signInWithUsernameAndPassword.router)
app.include_router(refreshToken.router)
