from fastapi import FastAPI
from routers import signInWithEmailAddressAndPassword, signInWithUsernameAndPassword, status

app = FastAPI()
app.include_router(status.router)
app.include_router(signInWithEmailAddressAndPassword.router)
app.include_router(signInWithUsernameAndPassword.router)
