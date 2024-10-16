from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton, QSpinBox, QTextEdit, QCompleter
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import pandas as pd


class OptionChoosingWidget(QWidget):
    def __init__(self, label: str, options: list):
        super().__init__()

        self.setLayout(QHBoxLayout())

        self.label_widget = LabelWidget(label)
        self.dropdown_widget = ComboBoxWidget(options)
        self.completer = QCompleter(options)

        self.dropdown_widget.setEditable(True)
        self.dropdown_widget.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.dropdown_widget.setCompleter(self.completer)

        self.dropdown_widget.setCurrentIndex(-1)

        self.layout().addWidget(self.label_widget)
        self.layout().addWidget(self.dropdown_widget)

        self.dropdown_widget.setStyleSheet("border: 1px solid #3E3E3E; background-color: white;")

    def update_options(self, options: list):
        self.dropdown_widget.clear()
        self.dropdown_widget.addItems(options)

        self.completer = QCompleter(options)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.dropdown_widget.setCompleter(self.completer)

        self.dropdown_widget.setCurrentIndex(-1)

    def get_options(self):
        return [self.dropdown_widget.itemText(i) for i in range(self.dropdown_widget.count())]

    def is_current_value_valid(self):
        valid_options = self.get_options()
        return self.get_current_value() in valid_options and self.dropdown_widget.currentIndex() != -1

    def get_current_value(self):
        return self.dropdown_widget.currentText()


class NumberSpinWidget(QWidget):
    def __init__(self, label: str, min_val: int, max_val: int, step_val: int):
        super().__init__()

        self.setLayout(QHBoxLayout())

        self.label_widget = LabelWidget(label)
        self.spin_box_widget = SpinBoxWidget(min_val, max_val, step_val)

        self.layout().addWidget(self.label_widget)
        self.layout().addWidget(self.spin_box_widget)
        self.spin_box_widget.setStyleSheet("background-color: white;")

    def get_value(self):
        return self.spin_box_widget.value()


class LabelWidget(QLabel):
    def __init__(self, label: str):
        super().__init__(label)


class ComboBoxWidget(QComboBox):
    def __init__(self, options_items: list):
        super().__init__()
        self.addItems(options_items)


class ButtonWidget(QPushButton):
    def __init__(self, text: str):
        super().__init__()

        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setEnabled(False)
        self.setFixedHeight(45)
        self.setStyleSheet("background-color: white;")


class SpinBoxWidget(QSpinBox):
    def __init__(self, minimum: int, maximum: int, step: int):
        super().__init__()

        self.setRange(minimum, maximum)
        self.setSingleStep(step)


class OutputTextEditWidget(QTextEdit):
    def __init__(self):
        super().__init__()

        self.setReadOnly(True)
        self.setStyleSheet('background-color: #F0E6B6; border: 1px solid black;')
        self.setPlaceholderText("Output")


class PlotCanvasWidget(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(6, 7))
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

    def plot_forecasts(self, actual_data, forecasts):
        self.axes.clear()

        self.axes.plot(actual_data.index, actual_data.values, label='Actual Data', color='blue')
        self.axes.plot([actual_data.index[-1], forecasts.index[0]],
                       [actual_data.values[-1], forecasts.values[0]],
                       color='red', linestyle='--')
        self.axes.plot(forecasts.index, forecasts.values, label='Forecasts', color='red')

        self.axes.set_xlabel('Date')
        self.axes.set_ylabel('Percent change')
        self.axes.set_title(actual_data.name)

        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.axes.xaxis.set_major_locator(mdates.AutoDateLocator())

        self.axes.set_facecolor('white')

        self.draw()
