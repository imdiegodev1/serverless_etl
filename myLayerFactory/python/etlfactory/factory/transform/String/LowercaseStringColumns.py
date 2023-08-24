from etlfactory.factory.transform.abs_transform import AbsTransform
import boto3
import time

class LowercaseStringColumns(AbsTransform):

    def execute(self, dfs: dict, table, parameters):
        """
        Removes leading and trailing spaces in the strings
        """
        df = dfs[table]
        columns = parameters['column_lst']
        try:
            for column in columns:
                df[column] = df[column].str.lower()

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
                        'message': (f"An error occurred while trying to apply query to the data frame {e}")
                    }
                ]
            )

            raise Exception(f"An error occurred while trying to apply query to the data frame {e}")

