import jwt,datetime,re

class CAutenticador:
    def __init__(self):
        None
    def Autenticar(self, event, context):

        tipo = event['type']
        token = event['authorizationToken']

        print('tipo=', tipo)

        print('token=', token)

        None

    def TokenGerar(self):

        payload = {

        "UserName":"Matheus",

        'exp': datetime.datetime.utcnow()

        }


        #Encode the payload

        secret = 'my-secret'

        encoded = jwt.encode(payload, secret, algorithm='HS256')


        request = {

        "authorizationToken" : encoded

        }  

        return request   
    
    def TokenHeadersObter(self, token):

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"  # Example: if sending JSON data
        }

        return 
