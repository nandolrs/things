from pymongo import MongoClient
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   #CONNECTION_STRING = "localhost:27017"# "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
   CONNECTION_STRING = "mongodb://nandolrs:12c7664!@docdb-cmj.cluster-cfiihtdzyscs.sa-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['estacao_list']
  
   # This is added so that many files can reuse the function get_database()
   if __name__ == "__main__":   
  
      # Get the database
      dbname = get_database()

