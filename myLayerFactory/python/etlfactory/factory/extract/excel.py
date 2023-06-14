from .abs_extraction import AbsExtraction
import pandas as pd
import sharepy

class ExtractExcel(AbsExtraction):
    def __init__(self, file_path):
        self.file_path = file_path
        self.connection = None

    def connect(self):
        sharepoint_url = 'https://itelbposmartsolutions.sharepoint.com/sites/DataScienceHub/'
        username = 'Reporting@Itelinternational.com'
        password = '_x4Le.wS:`s][PsF'
        self.sp = sharepy.SharePoint(sharepoint_url, username, password)
        self.sp.connect()
        print('connected to Sharepoint')

    def extract(self):
        file_name = self.file_path.split('/')[-1]
        self.sp.getfile(self.file_path, filename=file_name)
        df = pd.read_excel(file_name)
        print('extracted and saved in a byte object')
        return df
        