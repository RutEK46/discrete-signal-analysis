from MainView import MainView
from MainModel import MainModel
import os


class MainViewController:
    def __init__(self, folder_path='signals'):
        self.folder_path = folder_path

        self.view = MainView()
        self.model = MainModel()

        self.view.transformation_menu.options = self.model.transformation_names
        self.view.transformation_menu.value = None

        self.view.signal_file_menu.observe(self.on_signal_file_menu_change, 'value')

        self.view.input_signal_ploter = self.input_signal_ploter
        self.view.output_signal_ploter = self.output_signal_ploter

        self.view.signal_file_menu.options = self.file_names
        self.view.signal_file_menu.value = None

    @property
    def file_names(self):
        return [file_name for file_name in os.listdir(self.folder_path)
                if self.is_csv(self.get_file_path(file_name))]

    def on_signal_file_menu_change(self, *_):
        file_path = self.get_file_path(self.view.signal_file_menu.value)
        try:
            self.view.signal_key_menu.options = self.model.get_signal_keys(file_path) if file_path else []
        except FileNotFoundError:
            self.view.signal_file_menu.options = self.file_names
            self.view.signal_key_menu.options = []

    def input_signal_ploter(self, signal_file, signal_key, one_plot):
        self.model.plot_input_signal(self.get_file_path(signal_file), signal_key)

    def output_signal_ploter(self, signal_file, signal_key, transformation_name, one_plot):
        self.model.plot_output_signal(self.get_file_path(signal_file), signal_key, transformation_name, one_plot)

    def get_file_path(self, file_name):
        return f"{self.folder_path}/{file_name}"

    @staticmethod
    def is_csv(file_path):
        return file_path[-4:] == ".csv"
