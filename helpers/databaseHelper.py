from asyncpg import connect
from dotenv import load_dotenv
from os import getenv

load_dotenv()

async def getDatabaseConnection():
    try:
        connection = await connect(
            host=getenv("DATABASE_HOST"),
            database=getenv("DATABASE_NAME"),
            user=getenv("DATABASE_USER"),
            password=getenv("DATABASE_PASSWORD")
        )
        yield connection
    finally:
        await connection.close()
