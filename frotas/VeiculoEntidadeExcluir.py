import CFIotTwinMaker

def Testar():

    cEntity = CFIotTwinMaker.CEntity()

    retorno = cEntity.Consultar(workspaceId='VehicleFleetWorkspace1',entityName='MotorDC-entidade-v1r1')

    id = retorno['id']

    entidades = cEntity.Excluir(workspaceId='VehicleFleetWorkspace1',entityId=id)

Testar()  
print('testou')  