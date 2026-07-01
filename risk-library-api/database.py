from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"))

db = client[os.getenv("DATABASE_NAME")]

collection = db[os.getenv("COLLECTION_NAME")]

