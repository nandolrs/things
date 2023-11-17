# Get the database using the method we defined in pymongo_test_insert file
from estacao_get_database import get_database
from pandas import DataFrame

dbname = get_database()
 
collection_name = dbname["estacao_item"]
 
item_details = collection_name.find({"_id" : 1})

for item in item_details:
    
   print("item: ",item)

   temperatura = item["temperatura"]
   pressao = item["pressao"]
   altitude = item["altitude"]

   temperatura = temperatura + 1
   pressao = pressao + 1
   altitude =  altitude + 1

   item["temperatura"] = temperatura
   item["pressao"] = pressao
   item["altitude"] = altitude

   collection_name.update_one({"_id" : 1},{"$set" : item})

   print ("ok")