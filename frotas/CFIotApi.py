from typing import Union
from fastapi import FastAPI
import uvicorn


import boto3
import boto3.dynamodb.types
from boto3.dynamodb.conditions import Key, Attr

import CFVeiculos

# from pydantic import BaseModel
from typing import Union

#import json
from  decimal import Decimal

app = FastAPI()
app.openapi_version = "3.0.2"

@app.get("/api")
def read_root():
    return {"mensagem": "to aqui, pronto e saudável"}

# localhost:8000/api
# localhost:8000/api/pesquisar/esp8266-v1r1/2025-10-05T19:48:24.000Z/2025-10-05T19:48:24.000Z
# http://localhost:8000/docs
# http://localhost:8000/redoc
# http://localhost:8000/openapi.json
# https://169egekr7b.execute-api.sa-east-1.amazonaws.com/dev/api/pesquisar?placa=esp8266-v1r1&startTime=2025-10-05T19:48:00.000Z&endTime=2025-10-05T19:48:59.000Z

@app.get("/api/pesquisar/{placa}/{startTime}/{endTime}")
def pesquisar(placa:str, startTime:str, endTime:str):

    cVeiculos = CFVeiculos.CVeiculos()
    retorno  = cVeiculos.PesquisarPorPlacaDynamo(placa, startTime, endTime)  

    return retorno
    # return {"mensagem": "to aqui, pronto e saudável"}

def parse_float(value) :
    return Decimal(str(value))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


