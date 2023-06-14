from etlfactory.factory.transform.abs_transform import AbsTransform
import duckdb

class ApplyQuery(AbsTransform):

    def execute(self, dfs: dict, parameters, table = []):

        conn = duckdb.connect(':memory:')

        [conn.register(k, v) for k, v in dfs.items() if k in parameters["tables"]]

        result = conn.execute(parameters['query'])
        df = result.fetchdf()

        conn.close()

        return df
