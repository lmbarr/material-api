import re

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from constants import MONGO_URI


def get_mongo_db_connection():
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        raise e


def get_query_condition(minimal_density, maximal_density, exclude_elements, include_elements):
    list_conditions = []
    if minimal_density:
        list_conditions.append({'density': {'$gt': minimal_density}})

    if maximal_density:
        list_conditions.append({'density': {'$lt': maximal_density}})

    if exclude_elements:
        pattern = "|".join(map(re.escape, exclude_elements))
        regex = re.compile(pattern)
        list_conditions.append({'formula': {'$not': regex}})

    if include_elements:
        pattern = "|".join(map(re.escape, include_elements))
        regex = re.compile(pattern)
        list_conditions.append({'formula': regex})

    return list_conditions

