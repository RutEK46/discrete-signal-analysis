from MainView import MainView
from DefaultViewController import DefaultViewController
from InvestorViewController import InvestorViewController
from AggregateIndicatorGAViewController import AggregateIndicatorGAViewController
from macd import macd
from bollinger_bands import bollinger_bands


class MainViewController:
    def __init__(self, folder_path='signals'):
        self.view = MainView()

        self.aggregate_indicator_GA_view_controller = AggregateIndicatorGAViewController(folder_path=folder_path)

        transformations = {
            "aggregated": lambda signal: self.predict(signal, self.aggregate_indicator_GA_view_controller),
        }

        self.default_view_controller = DefaultViewController(folder_path=folder_path, transformations=transformations)
        self.investor_view_controller = InvestorViewController(folder_path=folder_path, transformations=transformations)

        self.children = [
            {
                "Controller": self.default_view_controller,
                "Name": "Standard",
            },
            {
                "Controller": self.investor_view_controller,
                "Name": "Investor",
            },
            {
                "Controller": self.aggregate_indicator_GA_view_controller,
                "Name": "Aggregate Indicator GA",
            },
        ]

        self.view.signals_tab.children = [child["Controller"].view.top_level for child in self.children]
        for i, child in enumerate(self.children):
            self.view.signals_tab.set_title(i, child["Name"])

    def predict(self, signal, view_controller):
        macd_ = [args for (*args,) in zip(*macd(signal))]
        bb = [args for (*args,) in zip(*bollinger_bands(signal))]
        list_ = list()
        for s, m, b in zip(signal, macd_, bb):
            value = view_controller.predict(s, m, b)
            if value is None:
                return None
            list_.append(value)
        return [list_]


