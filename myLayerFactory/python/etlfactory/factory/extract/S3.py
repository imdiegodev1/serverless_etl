from etlfactory.factory.extract.abs_extract import AbsExtract
import boto3
import pandas as pd
from datetime import datetime, timedelta

class S3(AbsExtract):

    def extract(self, parameters):

        self.connect()

        self.bucket_name = parameters['bucket_name']
        self.prefix = parameters['prefix'] + parameters.get('name','')
        self.file_name = parameters['file_name']

        if "days" in parameters:
            return self.df_generate_dates(parameters['days'])
        else:
            df = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.prefix+self.file_name)['Body']
            return [pd.DataFrame({}), pd.read_csv(df)]
        

    def connect(self):
        self.s3_client = boto3.client('s3')
    
    def df_generate_dates(self, days):
        dates = []
        today = datetime.now().date() # Obtiene la fecha actual
        
        for i in range(days):
            date = today - timedelta(days=i)
            date = f"{date.strftime('%Y-%m-%d')}/"
            dates.append(date) # Convierte la fecha al formato deseado
            
        # Recorre cada objeto en la respuesta
        dfs = []
        for date in dates:
            try:
                df = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.prefix+date+self.file_name)['Body']
            except:
                continue
            dfs.append(pd.read_csv(df))

        return [pd.DataFrame({}), pd.concat(dfs, join='outer')]

