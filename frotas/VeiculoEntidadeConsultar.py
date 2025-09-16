import CFIotTwinMaker

def Testar():

    cEntity = CFIotTwinMaker.CEntity()

    retorno = cEntity.Consultar(workspaceId='VehicleFleetWorkspace1'
                                    ,entityName = 'MotorDC-v3r1'
                                    )

    print(retorno)

Testar()  
print('testou')  