from .abs_validation import AbsValidation

import json
import pandas as pd
import pandera as pa
#from cerberus import Validator
#from datetime import datetime
import boto3
import os
from datetime import datetime

#from factory_etl.validation.invoice_validation import validation

class Validation(AbsValidation):

    def execute(self, dfs: dict, parameters: dict):
        
        dynamo_table = parameters['dynamo_table']
        table_key = parameters['table_key']
        search_key = parameters['search_key']

        dynamo_table_conn = self.connect_to_table(dynamo_table)
        dynamo_info = self.get_data_formats(dynamo_table_conn, table_key, search_key)

        last_schemas_updated = self.get_newest_register(dynamo_info['tables'])
        schemas = self.get_schemas(last_schemas_updated)

        validations = self.validation(schemas, dfs)
        
    def connect_to_table(self, dynamo_table:str):

        dynamo_conn = boto3.resource('dynamodb')
        dynamo_table_conn = dynamo_conn.Table(dynamo_table)

        return dynamo_table_conn
    
    def get_data_formats(self,
                         dynamo_table_conn,
                         dynamo_table_key: str,
                         search_key: str):

        data = dynamo_table_conn.get_item(
            Key={
                dynamo_table_key: search_key
            }
        )

        return data['Item']

    def get_newest_register(self,
                            dynamo_info: dict) -> dict:
        
        schema_dates = []

        for i in dynamo_info.keys():
            schema_dates.append(datetime.strptime(i, '%Y-%m-%d'))

        newest_metadata = max(schema_dates)

        return dynamo_info[newest_metadata.strftime("%Y-%m-%d")]

    def get_schemas(self,
                    schemas_dict: dict) -> dict:
        schemas = {}
        
        for i, j in schemas_dict.items():
            schemas[i] = eval(j)

        return schemas

    def validation(self,
                   schemas: dict,
                   dfs: dict):

        test_result = []

        for i in dfs.keys():
            try:
                print(f'validating: {i}')
                test = schemas[i].validate(dfs[i])
                test_result.append(test)
                print(f'Table {i} has the correct format.')
            except:
                schemas[i].validate(dfs[i])
                print('something went wrong')
                break

        return test_result