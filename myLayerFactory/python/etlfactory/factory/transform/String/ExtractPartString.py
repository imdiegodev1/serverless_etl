from etlfactory.factory.transform.abs_transform import AbsTransform
import boto3
import time

class ExtractPartString(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        df = dfs[table]
        string_origin = parameters['string_origin']
        string_from = parameters['string_from']
        string_until = parameters['string_until']
        new_column = parameters['new_column']

        print(type(string_from))
        print(type(string_until))

        try:
            df[new_column] = df[string_origin].str.slice(string_from, string_until)

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
                        'message': (f"Unable to lowercase string {e}")
                    }
                ]
            )

            raise Exception(f"Unable to lowercase string {e}")

        return df