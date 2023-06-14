from factory.transform.abs_transform import AbsTransform

class ChangeDataframeColumnsName(AbsTransform):

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

        df = dfs[table]

        try:
            df = df.rename(columns = parameters['map_columns'])
        except Exception as e:
            raise Exception(f"An error occurred while trying to change the column name {e}")

        return df
