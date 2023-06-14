from etlfactory.factory.transform.abs_transform import AbsTransform

class OrderDataframeColumns(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        df = dfs[table]

        df = df[parameters['columns']]

        return df
