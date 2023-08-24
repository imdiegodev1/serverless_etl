import pandas as pd

from etlfactory.factory.transform.abs_transform import AbsTransform


class DropDataframeColumns(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

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
            df = df.drop(columns=parameters['columns'], axis=1)
            return df
        except Exception as e:
            print('Error on execute method ', e)


