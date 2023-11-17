# Get the database using the method we defined in pymongo_test_insert file
from estacao_get_database import get_database
from pandas import DataFrame

# busca database
dbname = get_database()
 
# Retrieve a collection named "user_1_items" from database
collection_name = dbname["estacao_item"]
 
# consultar

item_details = collection_name.find({"_id" :1})

items_df = DataFrame(item_details)

print(items_df)
