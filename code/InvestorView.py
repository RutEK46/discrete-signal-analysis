import ipywidgets as widgets


class InvestorView:
    def __init__(self):
        self.text = widgets.Text("Hello World!!!")
        self.dropdown = widgets.Dropdown(options=["option1", "option2"])

        self.top_level = widgets.HBox(children=[
            self.text,
            self.dropdown,
        ])
