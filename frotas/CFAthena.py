import boto3

class CAThena:

    def __init__(self):
        self.cliente = boto3.client('athena')

    # def Incluir(self, bucketName, key, contentBody):
    #     try:
    #         self.cliente.put_object(Bucket=bucketName
    #                                 ,Key = key
    #                                 ,Body = contentBody)
        
    #     except Exception as e:
    #     #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
    #         raise    
    #  
    def ConsultarMetadadosTabela(self, CatalogName,DatabaseName,TableName,WorkGroup):
        try:

            # catalogo

            response = self.cliente.list_data_catalogs()
            for catalogo in response['DataCatalogsSummary']:
                print(catalogo['CatalogName'])


            # database

            response = self.cliente.list_databases(CatalogName=CatalogName)
            for database in response['DatabaseList']:
                print(database['Name'])

            # tables metadata

            response = self.cliente.list_table_metadata(CatalogName=CatalogName
                                                        ,DatabaseName=DatabaseName
                                                        )
            retorno = []
            for tabela in response['TableMetadataList']:
                nome = tabela['Name']
                if nome == TableName:
                    colunas = tabela['Columns']
                    for coluna in colunas:
                        nome = coluna['Name']
                        tipo = coluna['Type']
                        retorno.append({'nome':nome,'tipo':tipo})

            return retorno
            # # table metadata

            # response = self.cliente.get_table_metadata(CatalogName = CatalogName
            #                         ,DatabaseName = DatabaseName
            #                         ,TableName = TableName
            #                         ,WorkGroup = WorkGroup)
            
            # colunas = response.get
            # for tabelaMetadata in response['TableMetadata']:
            #     print(tabelaMetadata)            
        
        except Exception as e:
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise     


