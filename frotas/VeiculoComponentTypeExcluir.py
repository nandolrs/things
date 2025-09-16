import CFIotTwinMaker
import json

def Testar():

    cComponentType = CFIotTwinMaker.CComponentType()

    retorno = cComponentType.Excluir(
         workspaceId            = 'VehicleFleetWorkspace1'
        ,componentTypeId        = 'com.cmj.timeseries-connector'
    )

    print(retorno)

Testar()  
print('testou')  