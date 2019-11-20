from InvestorView import InvestorView
from InvestorModel import InvestorModel
import os


class InvestorViewController:
    def __init__(self, folder_path='signals', transformations={}):
        self.folder_path = folder_path

        self.view = InvestorView()
        self.model = InvestorModel()
        self.model.signal_transformations.update(transformations)

        self.view.signal_file_menu.options = sorted(self.file_names)

        self.view.signal_file_menu.observe(self.on_signal_file_menu_change, 'value')
        self.view.date_menu.observe(self.on_date_or_price_menu_change, 'value')
        self.view.signal_price_menu.observe(self.on_date_or_price_menu_change, 'value')


    @property
    def file_names(self):
        return [file_name for file_name in os.listdir(self.folder_path)
                if self.is_csv(self.get_file_path(file_name))]

    def get_file_path(self, file_name):
        return f"{self.folder_path}/{file_name}"

    @staticmethod
    def is_csv(file_path):
        return file_path[-4:] == ".csv"

    def get_data_menu(self):
        self.view.date_menu.options = self.model.get_all_data_reversed(
            self.get_file_path(self.view.signal_file_menu.value))

    def on_signal_file_menu_change(self, *_):
        try:
            self.get_data_menu()
            self.view.signal_price_menu.options = self.model.get_signal_keys(
                self.get_file_path(self.view.signal_file_menu.value))
            self.view.error_box.value = ""
        except KeyError:
            self.view.error_box.value = "ERROR: brak dat we wczytywanym pliku!"

    def on_date_or_price_menu_change(self, *_):
        if self.view.signal_price_menu.value is not None and self.view.date_menu.value is not None:
            self.view.decision1_answer.value = self.model.get_macd_decision(
                self.get_file_path(self.view.signal_file_menu.value),
                self.view.date_menu.value, self.view.signal_price_menu.value)

            self.view.decision2_answer.value = self.model.get_bollinger_bands_decision(
                self.get_file_path(self.view.signal_file_menu.value),
                self.view.date_menu.value, self.view.signal_price_menu.value)

            self.view.decision3_answer.value = self.model.get_stochastic_oscillator_decision(
                self.get_file_path(self.view.signal_file_menu.value),
                self.view.date_menu.value, self.view.signal_price_menu.value)

            self.view.agregated_decision_answer.value = self.model.get_agregated_decision(
                self.get_file_path(self.view.signal_file_menu.value),
                self.view.date_menu.value, self.view.signal_price_menu.value)




