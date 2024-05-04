from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

mongo_client = AsyncIOMotorClient(settings.mongo_host, settings.mongo_port, username=settings.mongo_username,
                                  password=settings.mongo_password)

mongo_db = mongo_client[settings.mongo_db]
mongo_collection = mongo_db[settings.mongo_collection]
