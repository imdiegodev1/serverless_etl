import pandas as pd
import boto3
import os
import boto3
import json
import io

from etlfactory.factory.extract.abs_extract import AbsExtract

class ExtractSQLServer(AbsExtract):

    def connect(self, parameters):
        lambda_client = boto3.client('lambda')

        payload = json.dumps(parameters)
        function_name = os.environ['GET_DATABASE_FILES']
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # Asynchronous invocation
            Payload=payload
        )

        response_dict = json.loads(response['Payload'].read().decode('utf-8'))
        print(response_dict.keys())
        self.address = response_dict['s3_url']

    def extract(self, parameters):

        self.connect(parameters)

        s3 = boto3.client('s3')
        file = s3.get_object(Bucket='datalakedsi', Key=self.address)
        data = file['Body'].read()
        df = pd.read_parquet(io.BytesIO(data))

        response_delete = s3.delete_object(Bucket='datalakedsi', Key=self.address)

        return None, df
