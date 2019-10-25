from collections.abc import Iterable
from pandas import read_csv
from fast_fourier_transformation import fast_fourier_transformation
from macd import macd
from bollinger_bands import bollinger_bands
from derivative import derivative
import logging as log
import plotly as py
import base_operations
import ipywidgets as widgets

py.offline.init_notebook_mode(connected=True)


class MainModel:

    # Allowed returns types of transformations:
    #   1) list
    #       1a) list made of Iterables (f. e. lists) - in this case it's transformation that returns more than
    #           one signal and each signal name must be defined in output_signal_names
    #       1b) otherwise - transformation that returns one signal
    #   2) Iterable (other than list) - same as 1b.
    signal_transformations = {
        "SMA": base_operations.sma,
        "Variation": base_operations.variation,
        "Standard deviation": base_operations.standard_deviation,
        "Energy": base_operations.energy,
        "Moment": base_operations.moment,
        "Central moment": base_operations.central_moment,
        "Standardized moment": base_operations.standardized_moment,
        "Standardized central moment" : base_operations.standardized_central_moment,
        "Fast Fourier Transformation": fast_fourier_transformation,
        "MACD": macd,
        "Bollinger Bands": bollinger_bands,
    }

    # Proper signals names for transformations that returns more than one signal
    # For transformations that returns only one signal - signal's name will be
    # transformation name
    # Order of names matters and must be same as order in which transformation
    # returns signals
    output_signal_names = {
        "MACD": ["MACD", "Signal"],
        "Bollinger Bands": ["Upper Band", "Middle Band", "Lower Band"],
    }

    # Any transformation parameter other in than signal must be defined here
    # Parameters are returned lambda function that takes signal as parameter,
    # what allows to adjust other parameters based on signal properties
    parameters = {
        "SMA": lambda signal: dict(
            span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal))
        ),
        "Variation": lambda signal: dict(
            span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)),
        ),
        "Standard deviation": lambda signal: dict(
            span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)),
        ),
        "Energy": lambda signal: dict(
            span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)),
        ),
        "Moment": lambda signal: dict(
            span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)),
            m=widgets.IntSlider(min=1, max=5, step=1, value=2),
        ),
        "Central moment": lambda signal: dict(
            span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)),
            m=widgets.IntSlider(min=1, max=5, step=1, value=2),
        ),
        "Standardized moment": lambda signal: dict(
            span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)),
            m=widgets.IntSlider(min=1, max=5, step=1, value=2),
        ),
        "Standardized central moment": lambda signal: dict(
            span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)),
            m=widgets.IntSlider(min=1, max=5, step=1, value=2),
        ),
        "MACD": lambda signal: dict(
            EMA1=widgets.IntSlider(min=1, max=100, step=1, value=12),
            EMA2=widgets.IntSlider(min=1, max=100, step=1, value=26),
            SIGNAL_EMA=widgets.IntSlider(min=1, max=100, step=1, value=9),
        ),
        "Bollinger Bands": lambda signal: dict(
            n=widgets.IntSlider(min=1, max=100, step=1, value=20),
            k=widgets.IntSlider(min=1, max=20, step=1, value=2),
        ),
    }

    colors = ['#0000FF', '#008b00', '#FF0000', "#222222"]

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

                if self.parameters.get(transformation):
                    widgets.interact(lambda **kwargs: self.__plot_output_signal(input_signal, transformation, **kwargs),
                                     **self.parameters[transformation](input_signal))
                else:
                    self.__plot_output_signal(input_signal, transformation)

            except Exception:
                log.exception("")
        else:
            print("")

    def get_signal_keys(self, file_path):
        csv_file = self.read_csv_file(file_path)

        return csv_file.keys() if csv_file is not None else []

    def __plot_output_signal(self, input_signal, transformation, **kwargs):
        try:
            output = self.signal_transformations[transformation](input_signal, **kwargs)

            if isinstance(output, list):
                if len(output) == 0:
                    print("")
                    return
                elif isinstance(output[0], list) or isinstance(output[0], Iterable):
                    traces = [dict(visible=True,
                                   line=dict(color=self.colors[i], width=1),
                                   name=self.output_signal_names.get(transformation)[i]
                                   if self.output_signal_names.get(transformation) else transformation,
                                   y=list(output_signal)) for i, output_signal in enumerate(output)]
                else:
                    traces = [dict(visible=True,
                                   line=dict(color=self.colors[0], width=1),
                                   name=self.output_signal_names.get(transformation)[0]
                                   if self.output_signal_names.get(transformation) else transformation,
                                   y=list(output))]
            elif isinstance(output, Iterable):
                traces = [dict(visible=True,
                               line=dict(color=self.colors[0], width=1),
                               name=self.output_signal_names.get(transformation)[0]
                               if self.output_signal_names.get(transformation) else transformation,
                               y=list(output))]
                if len(traces) == 0:
                    print("")
                    return
            else:
                print("")
                return

            py.offline.iplot(dict(data=dict(data=traces)))
        except Exception:
            log.exception("")
