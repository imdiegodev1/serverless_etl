#from etlfactory.factory.load.abs_load import AbsLoad
from .abs_load import AbsLoad
import boto3
import io
import pandas as pd

class Load(AbsLoad):


    def load(self, data, data_to_send):

        self.connect_s3()
        for key in data_to_send.keys():
            for parameters in data_to_send[key]:
                try:
                    if key == "RawData":

                        self.put_object(
                            bucket= parameters['bucket'],
                            key = f"{parameters['path']}{data[key][parameters['key']][0]['file_name']}",
                            body = data[key][parameters['key']][0]['contents'].getvalue()
                        )

                    else:

                        file_name = parameters['file_name']
                        df = data[key][parameters['key']]
                        dfs = {}

                        if 'column_date' in parameters:
                            for date, group in df.groupby(parameters['column_date']):
                                try:
                                    date = pd.to_datetime(date, format="%Y-%m-%d", errors="raise").strftime("%Y-%m-%d")
                                except:
                                    continue

                                dfs[f"{date}/{file_name}"] = group
                        else:
                                dfs[file_name] = df

                        # Acceder a los DataFrames individuales por fecha
                        for group, group_df in dfs.items():
                            with io.BytesIO() as parquet_buffer:

                                group_df.to_parquet(parquet_buffer, index=False)

                                self.put_object(
                                    bucket= parameters['bucket'],
                                    key = f"{parameters['path']}date_partition={group}",
                                    body = parquet_buffer.getvalue(),
                                    replace = parameters.get('replace','False')
                                )

                    print(f"key: {parameters['key']} - it worked")
                except Exception as e:
                    print("Error:", parameters['key'], e)

    def connect_s3(self):
        self.s3_client = boto3.client('s3')

    def put_object(self, bucket, key, body, replace = None):

        if replace == "False":
            try:
                self.s3_client.head_object(Bucket=bucket, Key=key)
                return None
            except:
                response = self.s3_client.put_object(
                    Bucket=bucket,
                    Key=key,
                    Body=body,
                )
        else:
            response = self.s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=body
            )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status != 200:
            print(f"Unsuccessful S3 put_object response. Status - {status}", key)
