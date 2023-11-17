from pymongo import MongoClient
 
# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "localhost:27017"# "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"

print ('passou 5')

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = MongoClient(CONNECTION_STRING)

print ('passou 6')
