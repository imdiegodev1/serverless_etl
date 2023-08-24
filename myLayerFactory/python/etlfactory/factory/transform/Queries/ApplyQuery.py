from etlfactory.factory.transform.abs_transform import AbsTransform
import duckdb
import boto3
import time


class ApplyQuery(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        try:

            conn = duckdb.connect(':memory:')

            [conn.register(k, v) for k, v in dfs.items() if k in parameters["tables"]]

            result = conn.execute(parameters['query'])
            df = result.fetchdf()

            conn.close()

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
                        'message': (f"An error occurred while trying to apply query to the data frame {e}")
                    }
                ]
            )

            raise Exception(f"An error occurred while trying to apply query to the data frame {e}")

        return df
