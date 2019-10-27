from InvestorView import InvestorView
from InvestorModel import InvestorModel


class InvestorViewController:
    def __init__(self, folder_path):
        self.folder_path = folder_path

        self.view = InvestorView()
        self.model = InvestorModel()
