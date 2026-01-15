from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]

projects = db["projects"]
skills = db["skills"]
templates = db["templates"]
runs = db["runs"]
