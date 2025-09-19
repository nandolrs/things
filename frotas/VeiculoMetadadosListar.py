import CFAthena

def Testar():

    cAthena = CFAthena.CAThena()

    CatalogName = "AwsDataCatalog"
    DatabaseName = 'cmj-database'
    TableName = 'tfrotas'
    WorkGroup = 'primary'
    retorno  = cAthena.ConsultarMetadadosTabela(CatalogName,DatabaseName,TableName,WorkGroup)

    print('===')
    print(retorno)




Testar()  
print('testou')  