from pymongo_get_database import get_database
from pymongo import MongoClient


dbname = get_database()

collection_name = dbname["user_1_items"]

print("1")

collection_name.create_index([("item_name", 1)]) #  pymongo.DESCENDING

print("2")

#collection_name.getIndexes()

#print("3")


#mongosh "mongodb+srv://mycluster.abcd1.mongodb.net/myFirstDatabase" --apiVersion 1 --username <username>

#mongosh "localhost:27017" --apiVersion 1 --username <username>

#mongosh "localhost:27017" --apiVersion 1
