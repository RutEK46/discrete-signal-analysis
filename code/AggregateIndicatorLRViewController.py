from AggregateIndicatorView import AggregateIndicatorView
from AggregateIndicatorModel import AggregateIndicatorModel
from sklearn.linear_model import LinearRegression
from contextlib import suppress
from itertools import islice
import pandas as pd
import os


class AggregateIndicatorLRViewController:
    key = "Zamkniecie"

    def __init__(self, folder_path):
        self.view = AggregateIndicatorView()
        self.model = AggregateIndicatorModel()

        self.linear_model = None

        self.view.on_list_of_files_change = self.model.print_file_names
        self.view.start_algorithm_button.on_click(self.on_start_algorithm_button_click)

        self.file_names = []

        self.view.folder_name_text.value = folder_path

    @property
    def learning_dataset(self):
        folder_path = self.view.folder_name_text.value
        self.file_names = os.listdir(folder_path)
        file_paths = [f"{folder_path}/{file_name}" for file_name in self.file_names]
        dataset = []
        for file_path in file_paths:
            with suppress(FileNotFoundError, KeyError):
                with open(file_path, 'r', encoding="ansi") as file:
                    csv_file = pd.read_csv(file)
                dataset.append(list(csv_file[self.key]))

        return dataset

    def on_start_algorithm_button_click(self, button):
        self.linear_regression()

    def linear_regression(self):
        __dataset = self.learning_dataset
        dataset = pd.DataFrame(columns=['MACD', 'Bollinger Bands', 'Signal'])

        for datum in __dataset:
            for i, (macd, bb) in islice(enumerate(zip(self._macd(datum), self._bollinger_bands(datum))), 35, len(datum) - 30):
                with suppress(IndexError):
                    dataset = dataset.append({
                        'MACD': macd,
                        'Bollinger Bands': bb,
                        'Signal': 1 if datum[i+1] > datum[i] else -1,
                    }, ignore_index=True)

        self.linear_model = LinearRegression()
        print(dataset.corr())
        self.linear_model.fit(dataset[['MACD', 'Bollinger Bands']].values, dataset['Signal'].values)

        templates = ["MACD: {}", "Bollinger Bands: {}", "Bias: {}"]
        coefs = list(self.linear_model.coef_) + [self.linear_model.intercept_]
        for template, coef, label in zip(templates, coefs, self.view.result_layer.children):
            label.value = template.format(coef)

        sum_earned = 0
        for datum in __dataset:
            X = [args for (*args,) in zip(self._macd(datum), self._bollinger_bands(datum))]
            current_money = 2000
            actions = 0
            predictions = self.linear_model.predict(X)
            for el, act in zip(datum, predictions):
                if act > 0:
                    new_actions = int(current_money / el)
                    actions += new_actions
                    current_money -= new_actions * el
                else:
                    current_money += actions * el
                    actions = 0
            current_money += actions * predictions[-1]
            sum_earned += current_money - 2000
        sum_earned /= len(__dataset)
        self.view.result_layer.children[-1].value = f"Earned: {sum_earned}"


    def predict(self, x, macd_result, bb_result):
        [u, m, _] = bb_result
        X = [self._macd_normalize(*macd_result), self._bollinger_bands_normalize(u, m, x)]
        return self.linear_model.predict([X])[0] if self.linear_model is not None else None

    def _macd(self, signal):
        [macd, signal] = self.model.signal_transformations["MACD"](signal)
        return (self._macd_normalize(m, s) for m, s in zip(macd, signal))

    def _bollinger_bands(self, signal):
        [upper, middle, _] = self.model.signal_transformations["Bollinger Bands"](signal)
        return (self._bollinger_bands_normalize(u, m, s) for u, m, s in zip(upper, middle, signal))

    @staticmethod
    def _macd_normalize(m, s):
        return m - s

    @staticmethod
    def _bollinger_bands_normalize(u, m, s):
        return (s - m) / (u - m) if u - m != 0 else 0
