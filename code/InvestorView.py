import ipywidgets as widgets


class InvestorView:
    def __init__(self):
        self.agregated_decision_name = widgets.Label("Agregated decision:")
        self.agregated_decision_answer = widgets.Label(value=None)
        self.agregated_decision = widgets.HBox(children=[
            self.agregated_decision_name,
            self.agregated_decision_answer,
        ])

        self.date_menu = widgets.Dropdown(
            value=None,
            description='Date:',
            options=[])

        self.signal_file_menu = widgets.Dropdown(
            value=None,
            description='Signals:',
        )

        self.signal_price_menu = widgets.Dropdown(
            value=None,
            description='Price:',
        )

        self.error_box = widgets.Label(value="")
        self.blank = widgets.Label("")

        self.decision1_name = widgets.Label("MACD(12,26,9):")
        self.decision1_answer = widgets.Label(value=None)
        self.decision1 = widgets.HBox(children=[
            self.decision1_name,
            self.decision1_answer,
        ])

        self.decision2_name = widgets.Label("Bollinger Bands:")
        self.decision2_answer = widgets.Label(value=None)
        self.decision2 = widgets.HBox(children=[
            self.decision2_name,
            self.decision2_answer,
        ])

        self.decision3_name = widgets.Label("Stochastic Oscillator:")
        self.decision3_answer = widgets.Label(value=None)
        self.decision3 = widgets.HBox(children=[
            self.decision3_name,
            self.decision3_answer,
        ])

        self.menu = widgets.VBox(children=[
            self.signal_file_menu,
            self.signal_price_menu,
            self.date_menu,
            self.blank,
            self.agregated_decision,
        ])

        self.top_level = widgets.VBox([
            self.menu,
            self.decision1,
            self.decision2,
            self.decision3,
            self.blank,
            self.error_box,
        ])
