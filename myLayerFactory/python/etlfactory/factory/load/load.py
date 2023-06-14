from .abs_load import AbsLoad

class Load(AbsExtraction):

    def connect_s3(self):
        print('connected to s3')

    def load_s3(self):
        print('load S3')