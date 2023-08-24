from etlfactory.factory.transform.abs_transform import AbsTransform
import boto3
import time

class OrderDataframeColumns(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        try:
            df = dfs[table]

            df = df[parameters['columns']]

        except Exception as e:

            session = boto3.Session()
            client = session.client('logs')

            STREAM_NAME = "Transform"

            log_response = client.put_log_events(
                logGroupName="DSI-Pipelines",
                logStreamName=STREAM_NAME,
                logEvents=[
                    {
                        'timestamp': int(round(time.time()*1000)),
                        'error message': (f"An error occurred while trying to order columns data frame {e}")
                    }
                ]
            )
            
            raise Exception(f"An error occurred while trying to order columns data frame {e}")


        return df
