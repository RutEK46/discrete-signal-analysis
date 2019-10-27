from collections.abc import Iterable
from pandas import read_csv
from SignalData import SignalData
import logging as log
import plotly as py
import ipywidgets as widgets

py.offline.init_notebook_mode(connected=True)


class DefaultModel(SignalData):
    colors = ['#0000FF', '#008b00', '#FF0000']
    input_signal_color = '#888888'

    def __init__(self):
        SignalData.__init__(self)
        self.transformation = None
        self.kw = {}

    def get_kwargs(self, transformation, input_signal):
        if self.transformation != transformation:
            self.transformation = transformation
            self.kw = self.parameters[transformation](input_signal)

        return self.kw

    def print_signal(self, file_path, key):
        if file_path and key:
            print('\n'.join(f"[{i}]: {element}" for i, element
                            in enumerate(self.read_csv_file(file_path)[key])))
        else:
            print("")

    def plot_input_signal(self, file_path, xkey, ykey):
        if file_path and xkey and ykey:
            input_x = list(self.read_csv_file(file_path)[xkey])
            input_signal = list(self.read_csv_file(file_path)[ykey])
            py.offline.iplot(dict(data=dict(data=self.get_traces(input_x, input_signal))))
        else:
            print("")

    def plot_output_signal(self, file_path, xkey, ykey, transformation, ad_input_signal_to_plot):
        if file_path and xkey and ykey and transformation:
            input_x = list(self.read_csv_file(file_path)[xkey])
            input_signal = list(self.read_csv_file(file_path)[ykey])

            def plot_func(**kwargs):
                try:
                    for key_, value in kwargs.items():
                        self.kw[key_].value = value
                    output = self.call_transformation(transformation, input_x, input_signal, kwargs)
                    traces = self.get_traces(input_x, input_signal if ad_input_signal_to_plot else None, output, transformation)
                    py.offline.iplot(dict(data=dict(data=traces)))
                except Exception:
                    log.exception("")

            if self.parameters.get(transformation):
                widgets.interact(plot_func, **self.get_kwargs(transformation, input_signal))
            else:
                plot_func()
        elif file_path and xkey and ykey and ad_input_signal_to_plot:
            self.plot_input_signal(file_path, xkey, ykey)
        else:
            print("")

    def get_signal_keys(self, file_path):
        csv_file = self.read_csv_file(file_path)

        return csv_file.keys() if csv_file is not None else []

    def get_traces(self, input_x, input_signal=None, output_signal=None, transformation=None):
        input_trace = [dict(visible=True,
                            line=dict(color=self.input_signal_color, width=1),
                            name=self.input_signal_name,
                            x=input_x,
                            y=input_signal)] if input_signal is not None else []

        if output_signal is None:
            return input_trace
        else:
            if isinstance(output_signal, list):
                if len(output_signal) == 0:
                    return input_trace
                elif isinstance(output_signal[0], list) or isinstance(output_signal[0], Iterable):
                    return [dict(visible=True,
                                 line=dict(color=self.colors[i], width=1),
                                 name=self.output_signal_names.get(transformation)[i]
                                 if self.output_signal_names.get(transformation) else transformation,
                                 x=input_x,
                                 y=list(out)) for i, out in enumerate(output_signal)] + input_trace
                else:
                    return [dict(visible=True,
                                 line=dict(color=self.colors[0], width=1),
                                 name=self.output_signal_names.get(transformation)[0]
                                 if self.output_signal_names.get(transformation) else transformation,
                                 x=input_x,
                                 y=list(output_signal))] + input_trace
            elif isinstance(output_signal, Iterable):
                return [dict(visible=True,
                             line=dict(color=self.colors[0], width=1),
                             name=self.output_signal_names.get(transformation)[0]
                             if self.output_signal_names.get(transformation) else transformation,
                             x=input_x,
                             y=list(output_signal))] + input_trace
            else:
                return input_trace
