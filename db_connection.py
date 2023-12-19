from dotenv import load_dotenv
import os
from pymongo import MongoClient
from fastapi import Request

load_dotenv()

# DB 저장을 위한 정보
DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")
COL_NAME = os.getenv("COL_NAME")

client = MongoClient(DB_URL)
db = client[DB_NAME]
collection = db[COL_NAME]

async def db_input_item(item: Request):
    item_dict = await item.json()
    print(type(item_dict))
    result = collection.insert_one(item_dict)
    inserted_id = str(result.inserted_id)
    return {"message": f"SKY {item_dict['last_sky_value']} PTY {item_dict['last_pty_value']} created with ID: {inserted_id}"}

def db_get(item):
    # 데이터 불러오기
    result = collection.find()
    first_document = result.next()

    _id_value = first_document.get('_id')

    result = collection.update_one({"_id": _id_value}, {"$set": item})    
