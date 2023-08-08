import pandas as pd

from etlfactory.factory.transform.abs_transform import AbsTransform


class DropDuplicatesDataframe(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        """Drop duplicates rows or registers

        Args:
            df (pd.DataFrame): The dataframe to be operated on.
        Raises:
            Exception: Raises exception when rename is not possible.

        Returns:
            [pd.DataFrame]: The Dataframe with unique rows or registers
        """
        try:
            df = dfs[table]
            df = df.drop_duplicates()
            return df
        except Exception as e:
            print('Error on execute method ', e)


