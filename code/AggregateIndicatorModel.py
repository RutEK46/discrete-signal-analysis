from SignalData import SignalData
import os


class IntegratedIndicatorModel(SignalData):
    def __init__(self):
        SignalData.__init__(self)
        self.folder_path = None

    def print_file_names(self, folder_path):
        try:
            self.folder_path = folder_path
            list_ = os.listdir(self.folder_path)
            print(f"Files in folder {self.folder_path}:")
            print('\n'.join(list_))
        except FileNotFoundError:
            self.folder_path = None
            print(f"There is no folder named {folder_path} !!!")
