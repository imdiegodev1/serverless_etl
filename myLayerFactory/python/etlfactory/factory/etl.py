import json
from etlfactory.factory.abs_factory import AbsFactory
from etlfactory.factory.loader import loader
from etlfactory.factory.transform.abs_transform import AbsTransform
from etlfactory.factory.extract.abs_extract import AbsExtract
from etlfactory.factory.load.abs_load import AbsLoad

class ETL_Factory(AbsFactory):
    def __init__(self, config) -> None:
        super().__init__()
        self.config = config
        self.data = {
            "RawData":{},
            "Dataframes":{}
        }

    def extract_method(self):

        for file in self.config["Extract"].keys():
            print("#####################################")
            print("Extracting File:", file)
            # if file not in self.data['RawData'] and file in self.config["Extract"].keys() :
            #         print(file)
            #         continue
            for method in self.config["Extract"][file].keys():

                path = self.config["Extract"][file][method]['path']
                module = loader(method, path, AbsExtract)
                raw_data, df = module.extract(self.config["Extract"][file][method]['parameters'])

                self.data['RawData'][file] = raw_data
                self.data['Dataframes'][file] = df
            print("Successfully extracted:", file)


    def transform_method(self):

        # Transform
        for file in self.config["Transform"].keys():
            for method in self.config["Transform"][file].keys():

                path = self.config["Transform"][file][method]['path']
                module = loader(method, path, AbsTransform)
                self.data['Dataframes'][file] = module.execute(
                    dfs = self.data['Dataframes'],
                    table = file,
                    parameters = self.config["Transform"][file][method]['parameters']
                )

        print(self.data)

    def load_method(self):

        # Load
        for method in self.config["Load"].keys():
            
            path = self.config["Load"][method]['path']
            data_to_send = self.config["Load"][method]['data_to_send']
            module = loader.loader(
                name = method, 
                package = path, 
                abstract = AbsLoad
            )

            return module.load(
                data = self.data,
                data_to_send = data_to_send
            )