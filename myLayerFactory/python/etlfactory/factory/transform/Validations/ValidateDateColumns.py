from etlfactory.factory.transform.abs_transform import AbsTransform

class ValidateDateColumns(AbsTransform):
    
    def execute(self, dfs: dict, table, parameters):
        '''
        Validate the date column from a dataframe, wrong values get deleted
        df= dataframe
        columns = list of columns name that need validation
        date_format = format date for to do validation
        '''

        df = dfs[table]

        try:
            for column in parameters['columns']:
                df[column] = df[column].astype('datetime64[ns]')
        except Exception as e:
            raise Exception(f"An error occurred while trying to validate and set the date column {e}")

        return df