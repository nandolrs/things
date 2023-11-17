# Get the database using the method we defined in pymongo_test_insert file
from estacao_get_database import get_database
from dateutil import parser

dbname = get_database()

collection_name = dbname["estacao_item"]

## insere colecoes

item = {
  "_id" :1
  , "temperatura" : 0
  , "pressao" : 0
  , "altitude" : 0
}

collection_name.insert_one(item)

print("ok")






