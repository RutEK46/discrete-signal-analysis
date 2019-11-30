from SignalData import SignalData
from macd import macd
from stochastic_oscillator import stochastic_oscillator
from bollinger_bands import bollinger_bands
from pandas import read_csv
from itertools import islice
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

    def print_full_indicators_decisions(self, signal_path, price_key):
        try:
            file = self.read_csv_file(signal_path)
            dates = list(file['Data'])
            prices = list(file[price_key])
            for indicator, func_dict in self.buys_sells_funcs.items():
                print(f"-----{indicator}-----")
                result = self.signal_transformations[indicator](prices)
                if result is not None:
                    for name, func in func_dict.items():
                        current_money = 2000
                        actions = 0
                        print(f"\t{name}:")
                        print(f"\t\t[{dates[0]}]starting money: {current_money}")

                        for (date, price, *args,) in islice(zip(dates, prices, *result), 5, None):
                            act = func(price, *args)
                            if act == 1:
                                new_actions = int(current_money / price)
                                if new_actions > 0:
                                    actions += new_actions
                                    current_money -= new_actions * price
                                    print("\t\t[{0}]Buys: {1} actions for {2:.2f}.".format(date, new_actions, price))
                            elif act == -1:
                                if actions > 0:
                                    current_money += actions * price
                                    print("\t\t[{0}]Sells: {1} actions for {2:.2f}.".format(date, actions, price))
                                    print("\t\t[{0}]Money: {1:.2f}.".format(date, current_money))
                                    actions = 0

                        end_sum = current_money + actions * prices[-1]
                        print("\t\t[{0}]Money at the end: {1:.2f}".format(dates[-1], end_sum))
        except Exception:
            print("")

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
        stochastic = stochastic_oscillator(input_signal)
        all_k = stochastic[0]
        min_k = min(all_k)
        max_k = max(all_k)
        today_k = stochastic[0][date_index]
        poziom = ((max_k - min_k) * 0.2)
        poziom_20 = min_k + poziom
        poziom_80 = max_k - poziom
        if today_k <= poziom_20:
            answer = "buy"
        elif today_k >= poziom_80:
            answer = "sell"
        else:
            answer = "neutral"
        return answer

    def get_agregated_decision(self, file_path, date, price):
        date_index = self.get_data_index(file_path, date)
        input_signal = list(self.read_csv_file(file_path)[price])

        return "neutral"
