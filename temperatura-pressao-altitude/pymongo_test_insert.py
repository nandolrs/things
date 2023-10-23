# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database
from dateutil import parser

dbname = get_database()

print("passou 11")

collection_name = dbname["user_1_items"]

print("passou 22")

## insere colecoes

item_1 = {
  "_id" : "U1IT00001",
  "item_name" : "Blender",
  "max_discount" : "10%",
  "batch_number" : "RR450020FRG",
  "price" : 340,
  "category" : "kitchen appliance"
}

print("passou 333")

item_2 = {
  "_id" : "U1IT00002",
  "item_name" : "Egg",
  "category" : "food",
  "quantity" : 12,
  "price" : 36,
  "item_description" : "brown country eggs"
}

print("passou 444")

##collection_name.insert_many([item_1,item_2])

print("passou 555")


expiry_date = '2021-07-13T00:00:00.000Z'
expiry = parser.parse(expiry_date)
item_3 = {
  "item_name" : "Bread",
  "quantity" : 2,
  "ingredients" : "all-purpose flour",
  "expiry_date" : expiry
}

print("passou 666")

#collection_name.insert_one(item_3)
collection_name.insert_many([item_1,item_2,item_3])

print("passou 777")






