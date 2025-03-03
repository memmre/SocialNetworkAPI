from datetime import datetime, timedelta
from dotenv import load_dotenv
from jwt import encode
from os import getenv
from passlib.context import CryptContext
from typing import Optional

load_dotenv()

ALGORITHM = "HS256"
SECRET_KEY = getenv("SECRET_KEY")
REFRESH_SECRET_KEY = getenv("REFRESH_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

cryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def createAccessToken(data: dict, expires_delta: Optional[timedelta] = None):
    toEncode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    toEncode.update({"exp": expire})
    return encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)

def createRefreshToken(data: dict, expires_delta: Optional[timedelta] = None):
    toEncode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    toEncode.update({"exp": expire})
    return encode(toEncode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
