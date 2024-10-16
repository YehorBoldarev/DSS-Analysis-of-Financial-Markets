import sys
from PyQt6.QtWidgets import QApplication
from UI.UiMain import MainWindow, GlobalFont
import warnings
warnings.filterwarnings('ignore')

from Helpers.DataHelper import DataHelper
from Steps.ModelsSteps import fit_models_by_sectors

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(GlobalFont())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# if __name__ == "__main__":
#     DataHelper().update_all_data()
#     fit_models_by_sectors()