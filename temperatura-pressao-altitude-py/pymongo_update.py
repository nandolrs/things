# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database
from pandas import DataFrame

dbname = get_database()
 
# Retrieve a collection named "user_1_items" from database
collection_name = dbname["user_1_items"]
 
# consultar

item_details = collection_name.find({"item_name" : "Blender"})

for item in item_details:
   # This does not give a very readable output
    print("item: ",item['item_name'])

    print(item['price'])

    preco = item['price']

    preco = preco+1

    item['price'] = preco

    #collection_name.update_one({"item_name" : "Blender"},{"$set" : {"price":343}})

    collection_name.update_one({"item_name" : "Blender"},{"$set" : item})

    print ("111")