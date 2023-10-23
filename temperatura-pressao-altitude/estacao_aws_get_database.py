import json
from pymongo import MongoClient
from dateutil import parser

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "localhost:27017"# "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
   #CONNECTION_STRING = "mongodb://nandolrs:12c7664!@docdb-cmj.cluster-cfiihtdzyscs.sa-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=/opt/python/global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
   #CONNECTION_STRING = "mongodb://nandolrs:12c7664!@docdb-cmj.cluster-cfiihtdzyscs.sa-east-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['estacao_list']
  
   # This is added so that many files can reuse the function get_database()
   if __name__ == "__main__":   
  
      # Get the database
      dbname = get_database()

def InserirOne():
    # Get the database using the method we defined in pymongo_test_insert file


    dbname = get_database()
    
    print('passou 11')

    collection_name = dbname["estacao_item"]
    
    print('passou 22')

    ## insere colecoes

    item = {
    "id" :222
    , "temperatura" : 0
    , "pressao" : 0
    , "altitude" : 0
    }

    print('passou 33')

    collection_name.insert_one(item)
    
    print('passou 44')


    print("ok")

def lambda_handler(event, context):


    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    dbname = get_database()

 
    print('passou 1')  

    InserirOne();

    print('passou 2')  


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!' )
    }

lambda_handler(1 , 2)