import pandas as pd

from etlfactory.factory.transform.abs_transform import AbsTransform


class SelectDataframeColumns(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        """Select a dataframe column names

        Args:
            df (pd.DataFrame): The dataframe to be operated on.
            map_columns (dict): A dictionary containing the select column names.

        Raises:
            Exception: Raises exception when select is not possible.

        Returns:
            [pd.DataFrame]: The Dataframe with the selected columns
        """
        try:
            df = dfs[table]
            df = df[parameters['columns']]
            return df
        except Exception as e:
            print('Error on execute method ', e)


