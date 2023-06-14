import pymssql
import pandas as pd

import os
#from dotenv import load_dotenv

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

        db_server = "itel-db-server.database.windows.net"
        db_name = "itel_datasi"
        db_user = "scripting"
        db_password = "0O%9d22lF$mIre6dCWue"
        self.conn = pymssql.connect(server = db_server, database = db_name, user = db_user, password = db_password)


    def get_query(self):
        with self.conn.cursor(as_dict=True) as cursor:
            cursor.execute("SELECT * FROM {schema}.{table} {where}".format(schema=self.schema, table=self.table, where=self.where))
            data = cursor.fetchall()
            df = pd.DataFrame(data)
        return None, df
