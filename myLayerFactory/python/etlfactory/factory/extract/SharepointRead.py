import pandas as pd
import os
from etlfactory.factory.extract.abs_extraction import AbsExtract
import office365.runtime.auth.user_credential as UserCredential
import office365.sharepoint.client_context as ClientContext
import office365.sharepoint.files.file as File
import os.path as get_path
import io
import boto3
import time
#from etlfactory.factory.extract.abs_extract import AbsExtract


class ExtractSharepoint(AbsExtract):
    def __init__(self):

        client = boto3.client('secretsmanager')

        self.url_sharepoint = client.get_secret_value(SecretId='url_sharepoint')['SecretString']
        self.username_sharepoint = client.get_secret_value(SecretId='username_sharepoint')['SecretString']
        self.password_sharepoint = client.get_secret_value(SecretId='password_sharepoint')['SecretString']
        self.log_group = 'DSI-Pipelines'
        self.stream_name = 'Extract'
        self.connect()

    def connect(self):
        """
            Function that stablish a connection with sharepoint

            Args:
                url_sharepoint
                username_sharepoint
                password_sharepoint

            Return:
                ctx: client context
        """
        try:
            self.ctx = ClientContext.ClientContext(self.url_sharepoint).with_credentials(
                UserCredential.UserCredential(self.username_sharepoint, self.password_sharepoint))
            print('Connected to Sharepoint')
        except Exception as e:
            session = boto3.Session()
            client = session.client('logs')

            log_response = client.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.stream_name,
                logEvents=[
                    {
                        'timestamp': int(round(time.time()*1000)),
                        'message': (f"An error ocurred while trying to connect to the data source {e}")
                    }
                ]
            )
            print('An error ocurred while trying to connect to the data source : ', e)

            raise Exception(f"An error ocurred while trying to connect to the data source {e}")

    def extract(self, parameters):
        try:
            self.load_method = parameters["load_method"]
            self.path_id = parameters["path_id"]
            self.folder_or_file = parameters["folder_or_file"]

            try:
                self.filename_in_column = parameters["file_name"]
            except:
                self.filename_in_column = False

            if self.folder_or_file == 'file':
                file_obj = self.get_sharepoint_file_by_id(self.path_id)
                self.raw_data = file_obj['contents']
                self.df = eval(self.load_method.format(file='file_obj["contents"]'))
            elif self.folder_or_file == 'folder':
                self.raw_data, self.df = self.extract_files_in_folder(self.path_id, self.filename_in_column)

            return [self.raw_data, self.df]
        except Exception as e:
            print(e)

    def get_sharepoint_file_by_id(self, file_id: str) -> dict:
        try:
            print('process get_sharepoint_file_by_id: {} ....'.format(file_id))
            sharepoint_contex = self.ctx
            file_obj = sharepoint_contex.web.get_file_by_id(file_id)
            sharepoint_contex.load(file_obj).execute_query()
            file_extension = get_path.splitext(file_obj.name)[1]
            file_name = file_obj.properties["Name"]
            file_contents = File.File.open_binary(sharepoint_contex, file_obj.serverRelativeUrl)
            if file_contents.status_code != 200:
                raise f"Couldn't fetch file with ID {file_id}"
            byte_stream = io.BytesIO(file_contents.content)
            data = {
                'contents': byte_stream,
                'extension': file_extension,
                'file_name': file_name
            }
            return data
        except Exception as e:
            session = boto3.Session()
            client = session.client('logs')

            log_response = client.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.stream_name,
                logEvents=[
                    {
                        'timestamp': int(round(time.time()*1000)),
                        'message': (f"Error on method get_sharepoint_file_by_id {e}")
                    }
                ]
            )

            print('Error on method get_sharepoint_file_by_id', e)

            raise Exception(f"Error on method get_sharepoint_file_by_id: {e}")

    def get_files_ids_in_folder(self, folder_id) -> list:
        try:
            print('proces get_files_ids_in_folder ....')
            folder_obj = self.ctx.web.get_folder_by_id(folder_id)
            self.ctx.load(folder_obj).execute_query()
            files_collection = folder_obj.files
            self.ctx.load(files_collection).execute_query()
            file_ids = [file.properties['UniqueId'] for file in files_collection]
            return file_ids
        except Exception as e:
            session = boto3.Session()
            client = session.client('logs')

            log_response = client.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.stream_name,
                logEvents=[
                    {
                        'timestamp': int(round(time.time()*1000)),
                        'message': (f"Error on method get_files_ids_in_folder: {e}")
                    }
                ]
            )

            print('Error on method get_files_ids_in_folder', e)

            raise Exception(f"Error on method get_files_ids_in_folder: {e}")

    def extract_files_in_folder(self, folder_id: str, filename_in_column: bool):

        if filename_in_column == False:
            try:
                print('Init extract_files_in_folder Process ....')
                file_ids = self.get_files_ids_in_folder(folder_id)
                dfs = []
                raw_data = []
                for file_id in file_ids:
                    file_obj = self.get_sharepoint_file_by_id(file_id)
                    raw_data.append(file_obj)
                    df = eval(self.load_method.format(file='file_obj["contents"]'))
                    dfs.append(df)
                df = pd.concat(dfs, ignore_index=True)
                return [raw_data, df]
            except Exception as e:
                session = boto3.Session()
                client = session.client('logs')

                log_response = client.put_log_events(
                    logGroupName=self.log_group,
                    logStreamName=self.stream_name,
                    logEvents=[
                        {
                            'timestamp': int(round(time.time()*1000)),
                            'message': (f"Error downloading files: {e}")
                        }
                    ]
                )
                
                print('Error downloading files: ', e)
                
                return [None, None]

        else:
            try:
                print('Init extract_files_in_folder Process ....')
                file_ids = self.get_files_ids_in_folder(folder_id)
                dfs = []
                raw_data = []
                for file_id in file_ids:
                    file_obj = self.get_sharepoint_file_by_id(file_id)
                    raw_data.append(file_obj)
                    df = eval(self.load_method.format(file='file_obj["contents"]'))
                    file_name = file_obj['file_name']
                    df['File_name'] = file_name
                    dfs.append(df)
                df = pd.concat(dfs, ignore_index=True)
                return [raw_data, df]

            except Exception as e:
                session = boto3.Session()
                client = session.client('logs')

                log_response = client.put_log_events(
                    logGroupName=self.log_group,
                    logStreamName=self.stream_name,
                    logEvents=[
                        {
                            'timestamp': int(round(time.time()*1000)),
                            'message': (f"Error downloading files: {e}")
                        }
                    ]
                )
                print('Error downloading files: ', e)
                return [None, None]
