from AggregateIndicatorView import AggregateIndicatorView
from AggregateIndicatorModel import AggregateIndicatorModel
from sigmoid import sigmoid
from genetic_algorithm import genetic_algorithm
from pandas import read_csv
from contextlib import suppress
from threading import Thread
from itertools import islice
import numpy as np
import os


class AggregateIndicatorGAViewController:
    key = "Zamkniecie"

    def __init__(self, folder_path):
        self.view = AggregateIndicatorView()
        self.model = AggregateIndicatorModel()

        self.view.on_list_of_files_change = self.model.print_file_names
        self.view.start_algorithm_button.on_click(self.on_start_algorithm_button_click)

        self.file_names = []
        self.best_chromosome = None

        self.view.folder_name_text.value = folder_path

    def on_start_algorithm_button_click(self, button):
        Thread(target=self.generic_algorithm()).start()

    def generic_algorithm(self):
        act_funcs = [
            self.activate_macd,
            self.activate_bollinger_bands,
            self.activate_bias
        ]

        dataset = self.learning_dataset
        templates = ["MACD: {}", "Bollinger Bands: {}", "Bias: {}"]

        max_earned = 0
        range_ = 16384
        for i, (chromosome, earned) in islice(enumerate(genetic_algorithm(dataset, act_funcs, 30, 0.005)), range_):
            if max_earned < earned:
                max_earned = earned
                self.best_chromosome = chromosome
                for template, coef, label in zip(templates, chromosome, self.view.result_layer.children):
                    label.value = template.format(coef)
                self.view.result_layer.children[-1].value = f"Earned: {earned}"
            self.view.progress.value = i/range_
        self.view.progress.value = 1

    def predict(self, x, macd_result, bb_result):
        if self.best_chromosome is not None:
            best_chromosome = np.array(self.best_chromosome)
            [u, m, _] = bb_result
            acts = [self._macd_normalize(*macd_result), self._bollinger_bands_normalize(u, m, x), 1]
            return sum(a * c for a, c in zip(acts, best_chromosome))
        else:
            return None


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
        return np.array(list(sigmoid(min(-m, (m - s)) for m, s in zip(macd, signal))), 'float64')

    def activate_bollinger_bands(self, signal):
        [upper, middle, _] = self.model.signal_transformations["Bollinger Bands"](signal)
        return np.array(list(sigmoid(-(s - m) / (u - m) if u - m != 0 else 0 for u, m, s in zip(upper, middle, signal))),
                        'float64')

    @staticmethod
    def activate_bias(signal):
        return np.array([1.0 for i in signal], 'float64')

    @staticmethod
    def _macd_normalize(m, s):
        return sigmoid(m - s)

    @staticmethod
    def _bollinger_bands_normalize(u, m, s):
        return sigmoid(-(s - m) / (u - m) if u - m != 0 else 0)
