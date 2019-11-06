from MainView import MainView
from DefaultViewController import DefaultViewController
from InvestorViewController import InvestorViewController
from AggregateIndicatorViewController import AggregateIndicatorViewController


class MainViewController:
    def __init__(self, folder_path='signals'):
        self.view = MainView()

        self.children = [
            {
                "Controller": DefaultViewController(folder_path=folder_path),
                "Name": "Standard",
            },
            {
                "Controller": InvestorViewController(folder_path=folder_path),
                "Name": "Investor",
            },
            {
                "Controller": AggregateIndicatorViewController(folder_path=folder_path),
                "Name": "Aggregate Indicator",
            }
        ]

        self.view.signals_tab.children = [child["Controller"].view.top_level for child in self.children]
        for i, child in enumerate(self.children):
            self.view.signals_tab.set_title(i, child["Name"])


