from .abs_extraction import AbsExtraction
import pandas as pd

class ExtractJson(AbsExtraction):
    def __init__(self, file_path):
        self.file_path = file_path
        self.connection = None
        
    def connect(self):
        self.connection = pd.read_json(self.file_path)
        print('connected to source')

    def extract(self):
        print('extracted and saved in a byte object')
        return self.connection        
        