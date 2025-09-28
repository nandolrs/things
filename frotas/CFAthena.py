import boto3
import time

class CAThena:

    def __init__(self):
        self.cliente = boto3.client('athena',region_name='us-east-1')

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

    def Pesquisar(self,DatabaseName, QUERY): # , CatalogName,DatabaseName,TableName,WorkGroup
        try:        
            response = self.cliente.start_query_execution(
                QueryString=QUERY,
                QueryExecutionContext={
                    'Database': DatabaseName # DATABASE
                }
                # ,
                # ResultConfiguration={
                #     'OutputLocation': ATHENA_OUTPUT_BUCKET
                # }
            )   

            query_execution_id = response['QueryExecutionId']     

            while True:

                response = self.cliente.get_query_execution(QueryExecutionId=query_execution_id)
                state = response['QueryExecution']['Status']['State']
                
                if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:  # (optional) checking the status 
                    break
                
                time.sleep(5)  # Poll every 5 seconds 

            # trata sucesso ou falha da consulta

            if state == 'SUCCEEDED':

                # Fetch the results if necessary
                result_data = self.cliente.get_query_results(QueryExecutionId=query_execution_id)

                retorno = {
                    'statusCode': 200,
                    'body': result_data
                }
                return retorno
            else:

                retorno = {
                    'statusCode': 400,
                    'body': f"Query {state}"
                }
                return retorno


        except Exception as e:
            print('== erro ==')
            print (e)            
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise               


