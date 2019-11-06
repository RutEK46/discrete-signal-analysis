import ipywidgets as widgets


class AggregateIndicatorView:
    def __init__(self):
        style = {'description_width': 'initial'}
        self.on_list_of_files_change = lambda **kwargs: None

        self.folder_name_text = widgets.Text(
            description="Folder Path:",
        )

        self.list_of_files_textarea = widgets.interactive_output(self.__on_list_of_files_change, {
            "folder_path": self.folder_name_text,
        })

        self.start_algorithm_button = widgets.Button(
            description="Start Genetic Algorithm"
        )

        self.result_layer = widgets.VBox([
            widgets.Text(
                description="MACD:",
                value="0%",
            ),
            widgets.Text(
                description="Bollinger Bands:",
                value="0%",
            ),
            widgets.Text(
                description="Bias:",
                value="0%",
            ),
        ])

        self.earned_text = widgets.Text(
            description="Earned:",
        )

        self.progress_text = widgets.Text(
            description="Generation number:"
        )

        self.progress_bar = widgets.FloatProgress(
            min=0,
            max=1,
            value=0,
        )

        self.top_level = widgets.VBox([
            self.folder_name_text,
            self.list_of_files_textarea,
            self.start_algorithm_button,
            self.result_layer,
            self.earned_text,
            self.progress_text,
            self.progress_bar,
        ], layout=widgets.Layout(width="100%"))

    def __on_list_of_files_change(self, **kwargs):
        self.on_list_of_files_change(**kwargs)
