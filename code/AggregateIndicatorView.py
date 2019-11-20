import ipywidgets as widgets


class AggregateIndicatorView:
    def __init__(self):
        self.on_list_of_files_change = lambda **kwargs: None

        self.folder_name_text = widgets.Text(
            description="Folder Path:",
        )

        self.list_of_files_textarea = widgets.interactive_output(self.__on_list_of_files_change, {
            "folder_path": self.folder_name_text,
        })

        self.start_algorithm_button = widgets.Button(
            description="Start"
        )

        self.result_layer = widgets.VBox([
            widgets.Label("MACD: "),
            widgets.Label("Bollinger Bands:"),
            widgets.Label("Bias:"),
            widgets.Label("Earned:"),
        ])

        self.name_label = widgets.Label()

        self.top_level = widgets.VBox([
            self.name_label,
            self.folder_name_text,
            self.list_of_files_textarea,
            self.start_algorithm_button,
            self.result_layer,
        ], layout=widgets.Layout(width="100%"))

    def __on_list_of_files_change(self, **kwargs):
        self.on_list_of_files_change(**kwargs)
