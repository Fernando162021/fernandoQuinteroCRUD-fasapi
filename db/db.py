import certifi
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get("MONGO_DB")
client = AsyncIOMotorClient(MONGO_URL, TLScafILE=certifi.where())
database = client["ing_swii"]
collection = database["libros"]
