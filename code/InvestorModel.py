from SignalData import SignalData
from macd import macd
from bollinger_bands import bollinger_bands
from pandas import read_csv
import logging as log


class InvestorModel(SignalData):
    def __init__(self):
        SignalData.__init__(self)
        self.file_path = None
        self.input_x = None

    def get_all_data(self, file_path):
        if file_path != self.file_path:
            self.input_x = list(self.read_csv_file(file_path)["Data"])
            self.file_path = file_path
        return self.input_x

    def get_all_data_reversed(self, file_path):
        lst = self.get_all_data(file_path)
        return lst[::-1]

    def get_data_index(self, file_path, date):
        data_list = self.get_all_data(file_path)
        index = data_list.index(date)
        return index

    def get_signal_keys(self, file_path):
        csv_file = self.read_csv_file(file_path)
        del csv_file["Data"]
        return csv_file.keys() if csv_file is not None else []

    def get_macd_decision(self, file_path, date, price):
        date_index = self.get_data_index(file_path, date)
        input_signal = list(self.read_csv_file(file_path)[price])
        macd_list = macd(input_signal, 12, 26, 9)
        macd_value = macd_list[0][date_index]
        signal_value = macd_list[1][date_index]
        if macd_value > signal_value:
            answer = "buy "
        elif macd_value == signal_value:
            answer = "neutral "
        else:
            answer = "sell "
        return answer + "(macd: " + "%.2f" % macd_value + ", signal: " + "%.2f" % signal_value + ")"

    def get_bollinger_bands_decision(self, file_path, date, price):
        date_index = self.get_data_index(file_path, date)
        input_signal = list(self.read_csv_file(file_path)[price])
        current_price = input_signal[date_index]
        bollinger_bands_list = bollinger_bands(input_signal)
        upper_band_value = bollinger_bands_list[0][date_index]
        middle_band_value = bollinger_bands_list[1][date_index]
        lower_band_value = bollinger_bands_list[2][date_index]
        if current_price < lower_band_value:
            answer = "buy "
        elif current_price > upper_band_value:
            answer = "sell "
        else:
            answer = "neutral "
        return answer + "(price: " + "%.2f" % current_price + ", upper_band_value: " + "%.2f" % upper_band_value \
               + ", middle_band_value: " + "%.2f" % middle_band_value + ", lower_band_value " \
               + "%.2f" % lower_band_value + ")"

    def get_stochastic_oscillator_decision(self, file_path, date, price):
        date_index = self.get_data_index(file_path, date)
        input_signal = list(self.read_csv_file(file_path)[price])
        return "TBD"

    def get_agregated_decision(self, file_path, date, price):
        date_index = self.get_data_index(file_path, date)
        input_signal = list(self.read_csv_file(file_path)[price])
        return "TBD"
