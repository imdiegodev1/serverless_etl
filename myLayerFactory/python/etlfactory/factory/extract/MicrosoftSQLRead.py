import pymssql
import pandas as pd
import boto3
import os
#from dotenv import load_dotenv
import boto3
import time

from etlfactory.factory.extract.abs_extract import AbsExtract

class ExtractSQLServer(AbsExtract):

    def extract(self, kwargs):
        self.schema = kwargs["schema"]
        self.table = kwargs["table"]
        try:
            self.where = kwargs["where"]
        except:
            self.where = ""
        self.connect()
        return self.get_query()

    def connect(self):

        #dotenv_path = "./.env"
        #load_dotenv(dotenv_path)
        client = boto3.client('secretsmanager')

        db_server = client.get_secret_value(SecretId='db_server')['SecretString']
        db_name = client.get_secret_value(SecretId='db_name')['SecretString']
        db_user = client.get_secret_value(SecretId='db_user')['SecretString']
        db_password = client.get_secret_value(SecretId='db_password')['SecretString']

        try:
            self.conn = pymssql.connect(server = db_server, database = db_name, user = db_user, password = db_password)
        except Exception as e:
            session = boto3.Session()
            client = session.client('logs')

            STRAM_NAME = "Extract"

            log_response = client.put_log_events(
                logGroupName="DSI-Pipelines",
                logStreamName=STRAM_NAME,
                logEvents=[
                    {
                        'timestamp': int(round(time.time()*1000)),
                        'message': (f"An error ocurred while trying to connect to the data source {e}")
                    }
                ]
            )

            raise Exception(f"An error ocurred while trying to connect to the data source {e}")


    def get_query(self):
        with self.conn.cursor(as_dict=True) as cursor:
            try:
                cursor.execute("SELECT * FROM {schema}.{table} {where}".format(schema=self.schema, table=self.table, where=self.where))
                data = cursor.fetchall()
                df = pd.DataFrame(data)
            except Exception as e:
                session = boto3.Session()
                client = session.client('logs')

                STRAM_NAME = "Extract"

                log_response = client.put_log_events(
                    logGroupName="DSI-Pipelines",
                    logStreamName=STRAM_NAME,
                    logEvents=[
                        {
                            'timestamp': int(round(time.time()*1000)),
                            'message': (f"An error ocurred while trying to excecute query {e}")
                        }
                    ]
                )

                raise Exception(f"An error ocurred while trying to excecute query {e}")
        return None, df
