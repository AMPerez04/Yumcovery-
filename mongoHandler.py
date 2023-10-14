from pprint import pprint

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from customDataClasses import User

uri = "mongodb+srv://amperez:fOiR1vg8RlQv49k2@yumcovery.nhon0ps.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))


def store_user(user: User):  # store user in db
    pass

