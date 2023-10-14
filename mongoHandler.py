import json
from pprint import pprint

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from customDataClasses import User

uri = "mongodb+srv://amperez:fOiR1vg8RlQv49k2@yumcovery.nhon0ps.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))


def store_user(user: User):  # store user in db
    pprint(client.UserHealthData.UserInfo.update_one({"name": user.name}, {"$set": user.__dict__}, upsert=True))


def get_activity(user: User):
    return client.UserHealthData.WearableData.find_one({"user.user_id": user.name})


def store_activity(activity):
    pprint(client.UserHealthData.WearableData.insert_one(activity))


pprint(get_activity(User("davidteju", 0, 0, 0, 0, 0)))
