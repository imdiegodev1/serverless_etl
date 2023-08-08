from etlfactory.factory.transform.abs_transform import AbsTransform
import re
import pandas as pd
import boto3
import time

class ExtractStringRegex(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        df = dfs[table]
        pattern = parameters['pattern']
        column = parameters['column_to_process']

        try:
            df[column] = df[column].str.extract(pattern)
            return df

        except Exception as e:

            session = boto3.Session()
            client = session.client('logs')

            log_message = str(e)

            log_response = client.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.log_stream,
                logEvents=[
                    {
                        'timestamp': int(round(time.time()*1000)),
                        'message': (f"Unable to extract string with regex pattern {e}")
                    }
                ]
            )

            raise Exception(f"Unable to extract string with regex pattern {e}")
