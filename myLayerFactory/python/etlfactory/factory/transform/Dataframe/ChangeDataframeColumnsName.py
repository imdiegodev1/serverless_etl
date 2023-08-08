from etlfactory.factory.transform.abs_transform import AbsTransform
import boto3
import time

class ChangeDataframeColumnsName(AbsTransform):
    
    def execute(self, dfs: dict,table,parameters):
        """Changes a dataframe column names
        Args:
            df (pd.DataFrame): The dataframe to be operated on.
            map_columns (dict): A dictionary containing the column rename mappings. Eg. {"old_name": "new_name"}
        Raises:
            Exception: Raises exception when rename is not possible.
        Returns:
            [pd.DataFrame]: The Dataframe with the renamed columns
        """
        try:
            df = dfs[table]
            df = df.rename(columns=parameters['map_columns'])
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
                        'message': (f"An error occurred while trying to change the name of columns {e}")
                    }
                ]
            )

            raise Exception(f"An error occurred while trying to change the name of columns {e}")

        return df

