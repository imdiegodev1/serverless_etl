from etlfactory.factory.transform.abs_transform import AbsTransform
import pandas as pd

class ConcatDataframes(AbsTransform):

    def execute(self, dfs: dict, table, parameters):
        '''
        Validate the duration columns from a dataframe, wrong values get deleted
        df = dataframe
        column = column name that need validation [LIST]
        regex = string for search match patterns and get hours, minutes and seconds
        '''
        
        new_df = []

        try:
            for df in parameters['dataframes']:
                if df not in dfs:
                    continue
                
                new_df.append(dfs[df])
                
        except Exception as e:
            raise Exception(f"An error occurred while trying to concatenate {e}")

        return pd.concat(new_df, ignore_index = True)