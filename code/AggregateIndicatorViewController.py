from AggregateIndicatorView import AggregateIndicatorView
from AggregateIndicatorModel import IntegratedIndicatorModel
from sigmoid import sigmoid
from genetic_algorithm import genetic_algorithm
from pandas import read_csv
from contextlib import suppress
from threading import Thread
from itertools import islice
import numpy as np
import os


class AggregateIndicatorViewController:
    key = "Zamkniecie"

    def __init__(self, folder_path):
        self.view = AggregateIndicatorView()
        self.model = IntegratedIndicatorModel()

        self.view.on_list_of_files_change = self.model.print_file_names
        self.view.start_algorithm_button.on_click(self.on_start_algorithm_button_click)

        self.file_names = []

        self.view.folder_name_text.value = folder_path

    def on_start_algorithm_button_click(self, button):
        Thread(target=self.generic_algorythm()).start()

    def generic_algorythm(self):
        act_funcs = [
            self.activate_macd,
            self.activate_bollinger_bands,
            self.activate_bias
        ]

        dataset = self.learning_dataset

        for i, (chromosome, earned) in islice(enumerate(genetic_algorithm(dataset, act_funcs, 8192, 0.5)), 1024):
            for result_text, weight in zip(self.view.result_layer.children, chromosome):
                result_text.value = f"{weight}"
            self.view.earned_text.value = str(earned)
            self.view.progress_text.value = str(i)

    @property
    def learning_dataset(self):
        folder_path = self.view.folder_name_text.value
        self.file_names = os.listdir(folder_path)
        file_paths = [f"{folder_path}/{file_name}" for file_name in self.file_names]
        dataset = []
        for file_path in file_paths:
            with suppress(FileNotFoundError, KeyError):
                with open(file_path, 'r', encoding="ansi") as file:
                    csv_file = read_csv(file)
                dataset.append(csv_file[self.key])

        min_len = min(len(datum) for datum in dataset)
        return np.array([[float(datum[i]) for i in range(min_len)] for datum in dataset], 'float64')

    def activate_macd(self, signal):
        [macd, signal] = self.model.signal_transformations["MACD"](signal)
        return np.array(list(sigmoid(m - s for m, s in zip(macd, signal))), 'float64')

    def activate_bollinger_bands(self, signal):
        [upper, middle, _] = self.model.signal_transformations["Bollinger Bands"](signal)
        return np.array(list(sigmoid((m - s) / u for u, m, s in zip(upper, middle, signal))), 'float64')

    @staticmethod
    def activate_bias(signal):
        return np.array([1.0 for i in signal], 'float64')
