from etlfactory.factory.transform.abs_transform import AbsTransform
import pandas as pd

class ConcatenateFields(AbsTransform):

    def concatenate_fields(self, dfs: dict, table, parameters):

        df = dfs[table]
        new_column = parameters['new_column']
        fields_to_concatenate = parameters['column_lst']
        df[new_column] = df[fields_to_concatenate].apply(' '.join, axis=1)

        return df