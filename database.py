from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from rich.console import Console
from models.customer import Customer

console = Console()

class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    # JWT
    secret_key: str
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        orm_mode = True

async def initiate_database():
    try:
        client = AsyncIOMotorClient(Settings().DATABASE_URL)
        console.log("client:", client)
        console.log('----------')
        db = client.get_default_database()
        console.log(db)
        await init_beanie(database=db, document_models=[Customer])
    except Exception as e:
        console.log("Error occurred:", e)

