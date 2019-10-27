from fast_fourier_transformation import fast_fourier_transformation
from macd import macd
from bollinger_bands import bollinger_bands
from derivative import derivative
from pandas import read_csv
import ipywidgets as widgets
import base_operations


class SignalData:
    def __init__(self):
        # Allowed returns types of transformations:
        #   1) list
        #       1a) list made of Iterables (f. e. lists) - in this case it's transformation that returns more than
        #           one signal and each signal name must be defined in output_signal_names
        #       1b) otherwise - transformation that returns one signal
        #   2) Iterable (other than list) - same as 1b.
        self.signal_transformations = {
            "SMA": base_operations.sma,
            "Variation": base_operations.variation,
            "Standard deviation": base_operations.standard_deviation,
            "Energy": base_operations.energy,
            "Moment": base_operations.moment,
            "Central moment": base_operations.central_moment,
            "Standardized moment": base_operations.standardized_moment,
            "Standardized central moment": base_operations.standardized_central_moment,
            "FFT": fast_fourier_transformation,
            "MACD": macd,
            "Bollinger Bands": bollinger_bands,
        }

        self.signal_transformations_with_x_input = {
            "Derivative": derivative,
        }

        # Proper signals names for transformations that returns more than one signal
        # For transformations that returns only one signal - signal's name will be
        # transformation name
        # Order of names matters and must be same as order in which transformation
        # returns signals
        self.output_signal_names = {
            "MACD": ["MACD", "Signal"],
            "Bollinger Bands": ["Upper Band", "Middle Band", "Lower Band"],
        }
        self.input_signal_name = "Input"

        # Any transformation parameter other in than signal must be defined here
        # Parameters are returned by lambda function that takes signal as parameter,
        # what allows to adjust other parameters based on signal properties
        self.parameters = {
            "SMA": lambda signal: dict(
                span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)/2, continuous_update=False),
            ),
            "Variation": lambda signal: dict(
                span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)/2, continuous_update=False),
            ),
            "Standard deviation": lambda signal: dict(
                span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)/2, continuous_update=False),
            ),
            "Energy": lambda signal: dict(
                span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)/2, continuous_update=False),
            ),
            "Moment": lambda signal: dict(
                span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)/2, continuous_update=False),
                m=widgets.IntSlider(min=1, max=5, step=1, value=2, continuous_update=False),
            ),
            "Central moment": lambda signal: dict(
                span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)/2, continuous_update=False),
                m=widgets.IntSlider(min=1, max=5, step=1, value=2, continuous_update=False),
            ),
            "Standardized moment": lambda signal: dict(
                span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)/2, continuous_update=False),
                m=widgets.IntSlider(min=1, max=5, step=1, value=2, continuous_update=False),
            ),
            "Standardized central moment": lambda signal: dict(
                span=widgets.IntSlider(min=1, max=len(signal), step=1, value=len(signal)/2, continuous_update=False),
                m=widgets.IntSlider(min=1, max=5, step=1, value=2, continuous_update=False),
            ),
            "MACD": lambda signal: dict(
                EMA1=widgets.IntSlider(min=1, max=100, step=1, value=12, continuous_update=False),
                EMA2=widgets.IntSlider(min=1, max=100, step=1, value=26, continuous_update=False),
                SIGNAL_EMA=widgets.IntSlider(min=1, max=100, step=1, value=9, continuous_update=False),
            ),
            "Bollinger Bands": lambda signal: dict(
                n=widgets.IntSlider(min=1, max=100, step=1, value=20, continuous_update=False),
                k=widgets.IntSlider(min=1, max=20, step=1, value=2, continuous_update=False),
            ),
        }

        self.csv_file_path = None
        self.csv_file = None

    def read_csv_file(self, file_path):
        if not file_path:
            self.csv_file_path = None
            self.csv_file = None
            return None

        elif file_path != self.csv_file_path:
            self.csv_file = read_csv(file_path)
            self.csv_file_path = file_path

        return self.csv_file

    @property
    def transformation_names(self):
        return list(self.signal_transformations.keys()) + list(self.signal_transformations_with_x_input.keys())

    def call_transformation(self, name, X, Y, kwargs):
        try:
            return self.signal_transformations[name](Y, **kwargs)
        except KeyError:
            return self.signal_transformations_with_x_input[name](X, Y, **kwargs)
