import boto3

class CS3:

    def __init__(self):
        self.cliente = boto3.client('s3')

    def Incluir(self, bucketName, key, contentBody):
        try:
            self.cliente.put_object(Bucket=bucketName
                                    ,Key = key
                                    ,Body = contentBody)
        
        except Exception as e:
        #   logger.error(f"Failed to upload receipt to S3: {str(e)}")
            raise     


