from etlfactory.factory.transform.abs_transform import AbsTransform
import pandas as pd

class GruopByDataframe(AbsTransform):

    def execute(self, dfs: dict, table, parameters):
        df = dfs[table]
        pass