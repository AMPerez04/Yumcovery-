from pprint import pprint

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from customDataClasses import User

uri = "mongodb+srv://amperez:fOiR1vg8RlQv49k2@yumcovery.nhon0ps.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))


def store_user(user: User):  # store user in db
    pprint(client.UserHealthData.UserInfo.update_one({"name": user.name}, {"$set": user.__dict__}, upsert=True))


def get_activity(user_id: str):
    return client.UserHealthData.WearableData.find_one({"user.user_id": user_id})


def store_activity(activity):
    pprint(client.UserHealthData.WearableData.insert_one(activity))


def get_user(user_id: str):
    return client.UserHealthData.UserInfo.find_one({"name": user_id})


def get_nutrition_ingested(user_id: str):
    pass
