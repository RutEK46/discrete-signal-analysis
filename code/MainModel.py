from pandas import read_csv
from fast_fourier_transformation import fast_fourier_transformation
from macd import macd
import logging as log
import plotly as py

py.offline.init_notebook_mode(connected=True)


class MainModel:
    signal_transformations = {
        "Fast Fourier Transformation": lambda y: [[abs(value) for value in fast_fourier_transformation(y)]],
        "MACD": macd,
    }

    output_signal_names = {
        "MACD": ["MACD", "Signal"],
    }

    colors = ['#0000FF', '#00FF00']

    def __init__(self):
        self.csv_file_path = None
        self.csv_file = None

    @property
    def transformation_names(self):
        return self.signal_transformations.keys()

    def read_csv_file(self, file_path):
        if not file_path:
            self.csv_file_path = None
            self.csv_file = None
            return None

        elif file_path != self.csv_file_path:
            self.csv_file = read_csv(file_path)
            self.csv_file_path = file_path

        return self.csv_file

    def print_signal(self, file_path, key):
        if file_path and key:
            print('\n'.join(f"[{i}]: {element}" for i, element
                            in enumerate(self.read_csv_file(file_path)[key])))
        else:
            print("")

    def plot_input_signal(self, file_path, key):
        if file_path and key:
            trace = dict(visible=True,
                         line=dict(color='#000000', width=1),
                         name='Plot',
                         y=list(self.read_csv_file(file_path)[key]))

            py.offline.iplot(dict(data=dict(data=[trace])))
        else:
            print("")

    def plot_output_signal(self, file_path, key, transformation):
        if file_path and key and transformation:
            try:
                input_signal = [element for element in self.read_csv_file(file_path)[key]]
                output_signals = self.signal_transformations[transformation](input_signal)

                traces = [dict(visible=True,
                               line=dict(color=self.colors[i], width=1),
                               name=self.output_signal_names.get(transformation)[i]
                               if self.output_signal_names.get(transformation) else transformation,
                               y=output_signal) for i, output_signal in enumerate(output_signals)]

                py.offline.iplot(dict(data=dict(data=traces)))
            except Exception:
                log.exception("")
        else:
            print("")

    def get_signal_keys(self, file_path):
        csv_file = self.read_csv_file(file_path)

        return csv_file.keys() if csv_file is not None else []




