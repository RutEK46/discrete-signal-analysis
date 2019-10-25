import ipywidgets as widgets


class MainView:
    def __init__(self):
        self.input_signal_printer = lambda signal_file, signal_key: None
        self.input_signal_ploter = lambda signal_file, signal_key: None
        self.output_signal_ploter = lambda signal_file, signal_key, transformation_name: None

        self.signal_file_menu = widgets.Dropdown(
            value=None,
            description='Signals:',
        )

        self.signal_key_menu = widgets.Dropdown(
            value=None,
            description='Keys:',
        )

        self.transformation_menu = widgets.Dropdown(
            value=None,
            description='Transformations:',
        )

        self.input_signal = widgets.interactive_output(lambda **kwargs: self.input_signal_printer(**kwargs), {
            'signal_file': self.signal_file_menu,
            'signal_key': self.signal_key_menu,
        })

        self.input_signal_plot = widgets.interactive_output(lambda **kwargs: self.input_signal_ploter(**kwargs), {
            'signal_file': self.signal_file_menu,
            'signal_key': self.signal_key_menu,
        })

        self.signal_output_plot = widgets.interactive_output(lambda **kwargs: self.output_signal_ploter(**kwargs), {
            'signal_file': self.signal_file_menu,
            'signal_key': self.signal_key_menu,
            'transformation_name': self.transformation_menu,
        })

        layout = widgets.Layout(grid_template_columns='1fr 1fr')
        plot_grid_box = widgets.GridBox(layout=layout, children=[
            self.input_signal_plot,
            self.signal_output_plot,
        ])

        signal_accordion = widgets.Accordion(children=[self.input_signal])
        signal_accordion.set_title(0, 'Signal')

        self.top_level = widgets.VBox([
            self.signal_file_menu,
            self.signal_key_menu,
            self.transformation_menu,
            plot_grid_box,
            signal_accordion,
        ])
