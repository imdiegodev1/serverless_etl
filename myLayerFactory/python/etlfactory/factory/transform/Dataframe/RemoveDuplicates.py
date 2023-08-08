from etlfactory.factory.transform.abs_transform import AbsTransform
import pandas as pd
import boto3
import time

class RemoveDuplicates(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        df = dfs[table]
        remove_duplicates_from = parameters['remove_duplicates_from']
        try:
            df = df.drop_duplicates(subset=remove_duplicates_from)
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
                        'message': (f"An error occurred while trying remove duplicates {e}")
                    }
                ]
            )

            raise Exception(f"An error occurred while trying remove duplicates {e}")
