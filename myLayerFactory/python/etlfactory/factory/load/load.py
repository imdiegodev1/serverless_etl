from etlfactory.factory.load.abs_load import AbsLoad
import boto3
import io
import os
import fastparquet as fp
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
                            parquet_buffer = self.convert_to_parquet(group_df)
                            #with io.BytesIO() as parquet_buffer:

                            #    group_df.to_parquet(parquet_buffer, index=False)

                            self.put_object(
                                bucket= parameters['bucket'],
                                key = f"{parameters['path']}date_partition={group}",
                                body = parquet_buffer.getvalue(),
                                replace = parameters.get('replace','True')
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


    def convert_to_parquet(self, df):

        data_type_mapping = {
            "mixed-integer": "int",
            "mixed-integer-float": "float",
            "string": "str",
            "integer": "int",
            "datetime64": "datetime64",
            "categorical": "category",
            "boolean": "bool",
            "unicode": "unicode",
            "timedelta64": "timedelta64",
            "string": "str",
            "floating": "float",
            "decimal": "float",
            "datetime": "datetime64",
            "date": "datetime64",
            "time": "datetime64",
            "timedelta": "timedelta64",
            "timedelta64": "timedelta64",
            "empty": "str",
            "period": "timedelta64",
            "mixed": "str"
        }

        data_types = {}
        for col in df.columns:
            inferred_type = pd.api.types.infer_dtype(df[col])
            data_types[col] = inferred_type

        for col, inferred_type in data_types.items():
            if inferred_type in data_type_mapping:
                dtype = data_type_mapping[inferred_type]
                if dtype == "datetime64":
                    df[col] = pd.to_datetime(df[col])
                elif dtype == "timedelta64":
                    df[col] == pd.to_timedelta(df[col])
                else:
                    df[col] = df[col].astype(dtype)
            else:
                print("error")
                print("missing type:", inferred_type)

        parquet_buffer = io.BytesIO()
        temp_file_path = '/tmp/temp_file.parquet'
        fp.write(temp_file_path, df, compression='GZIP')
        with open(temp_file_path, 'rb') as f:
            parquet_buffer.write(f.read())

        os.remove(temp_file_path)

        return parquet_buffer
