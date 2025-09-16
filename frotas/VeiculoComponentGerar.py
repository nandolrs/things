import CFIotTwinMaker

def Testar():

    cComponent = CFIotTwinMaker.CComponent()

    retorno = cComponent.Gerar(
            nome='MotorDC-componente-01'
            ,componentTypeId='com.cmj.timeseries-connector-v1r1'
    )

    print(retorno)

Testar()  
print('testou')  