# Get the database using the method we defined in pymongo_test_insert file
from estacao_get_database import get_database
from pandas import DataFrame

# obtem json

_json = {"estacao":
         {
            "temperatura":11
            ,"pressao":22
            ,"altitude":33
          }
         }

# pega os valores do json

temperatura = _json['estacao']['temperatura']
pressao = _json['estacao']['pressao']
altitude = _json['estacao']['altitude']


# atualiza banco

dbname = get_database()
 
collection_name = dbname["estacao_item"]
 
item_details = collection_name.find({"_id" : 1})

for item in item_details:
    
   print("item: ",item)

   item["temperatura"] = temperatura
   item["pressao"] = pressao
   item["altitude"] = altitude

   collection_name.update_one({"_id" : 1},{"$set" : item})

   print ("ok")