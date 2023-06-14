import pandas as pd

# import sharepy
# from io import BytesIO
import os.path as get_path
import io

import office365.runtime.auth.user_credential as uc
import office365.sharepoint.client_context as cc
import office365.sharepoint.files.file as file

from etlfactory.factory.extract.abs_extract import AbsExtract

class SharepointRead(AbsExtract):

    def extract(self, parameters):
        self.url = 'https://itelbposmartsolutions.sharepoint.com/sites/DataScienceHub/'
        self.username = 'Reporting@Itelinternational.com'
        self.password = '_x4Le.wS:`s][PsF'


        self.load_method = parameters['load_method']
        self.path_id = parameters['path_id']
        self.folder_or_file = parameters['folder_or_file']

        self.connect()

        if self.folder_or_file == 'file':
            file_obj = self.get_sharepoint_file_by_id(self.path_id)
            self.raw_data = file_obj['contents']
            self.df = eval(self.load_method.format(file = 'file_obj["contents"]'))
        elif self.folder_or_file == 'folder':
            self.raw_data, self.df = self.extract_files_in_folder(self.path_id)

        return [self.raw_data, self.df]


    def connect(self) -> cc.ClientContext:
        self.ctx = cc.ClientContext(self.url).with_credentials(uc.UserCredential(self.username, self.password))


    def get_sharepoint_file_by_id(self, file_id: str) -> dict:

        file_obj = self.ctx.web.get_file_by_id(file_id)
        self.ctx.load(file_obj).execute_query()
        file_extension = get_path.splitext(file_obj.name)[1]
        file_name = file_obj.properties["Name"]
        file_contents = file.File.open_binary(self.ctx, file_obj.serverRelativeUrl)
        if file_contents.status_code != 200:
            raise f"Couldn't fetch file with ID {file_id}"
        byte_stream = io.BytesIO(file_contents.content)
        data = {
            'contents': byte_stream,
            'extension': file_extension,
            'file_name': file_name
        }
        return data


    def get_files_ids_in_folder(self, folder_id: str) -> list:

        folder_obj = self.ctx.web.get_folder_by_id(folder_id)
        self.ctx.load(folder_obj).execute_query()
        files_collection = folder_obj.files
        self.ctx.load(files_collection).execute_query()
        file_ids = [file.properties['UniqueId'] for file in files_collection]
        return file_ids


    def extract_files_in_folder(self, folder_id: str):
        try:
            file_ids = self.get_files_ids_in_folder(folder_id)
            dfs = []
            raw_data = []
            for file_id in file_ids:
                file_obj = self.get_sharepoint_file_by_id(file_id)
                raw_data.append(file_obj)
                df = eval(self.load_method.format(file = 'file_obj["contents"]'))
                dfs.append(df)
            df = pd.concat(dfs, ignore_index = True)
            # ---- create and get temporal path
            #path_extraction = create_folder(self.parameters["relative_folder"], self.parameters["file_name"])
            # ---- Write file in temporal path
            #df.to_csv(path_extraction, sep = ",", index = False)
            return [raw_data, df]
        except Exception as e:
            print(e)
            return [None, None]
            #raise e
