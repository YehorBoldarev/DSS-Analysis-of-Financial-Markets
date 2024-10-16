from datetime import datetime
from PyQt6.QtWidgets import QVBoxLayout, QFrame
from PyQt6.QtGui import QFont
from UI.UiWidgets import *
from Providers.DbProvider import DataProvider
from Steps.ModelsSteps import forecast_for_sector, forecast_for_industry, forecast_for_asset
from Helpers.OutputHelper import aggregate_industry_forecast_results, aggregate_sector_forecast_results
from UI.UiWorker import Worker
from PyQt6.QtCore import QThreadPool


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Комплексний аналіз фінансового ринку")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #DCE0D9;")

        self.data_provider = DataProvider()

        layout = QHBoxLayout()

        '''Input side build'''
        self.input_frame = QFrame()
        self.input_frame.setFixedWidth(int(1280 * 0.7))
        input_frame_layout = QVBoxLayout()

        self.start_button = ButtonWidget("Start!")
        self.start_button.clicked.connect(self.trigger_start)

        self.analyze_type_def_box = OptionChoosingWidget("Type:", ["Sector", "Industry", "Asset"])
        self.analyze_type_def_box.dropdown_widget.setEditable(False)
        self.analyze_type_def_box.dropdown_widget.currentIndexChanged.connect(self.update_input_fields)
        self.analyze_type_def_box.dropdown_widget.currentIndexChanged.connect(self.verify_inputs_validity)

        sector_names = self.data_provider.get_sector_names_list()
        self.sector_def_box = OptionChoosingWidget("Sector:", sector_names)
        self.sector_def_box.hide()
        self.sector_def_box.dropdown_widget.currentIndexChanged.connect(
            lambda index: self.update_by_sector(index, sector_names))
        self.sector_def_box.dropdown_widget.currentTextChanged.connect(self.verify_inputs_validity)

        industry_names = self.data_provider.get_industry_names_by_sector(self.sector_def_box.get_current_value())
        self.industry_def_box = OptionChoosingWidget("Industry:", industry_names)
        self.industry_def_box.hide()
        self.industry_def_box.dropdown_widget.currentTextChanged.connect(self.verify_inputs_validity)

        asset_tickers = self.data_provider.get_all_companies()
        self.asset_def_box = OptionChoosingWidget("Asset's ticker:", asset_tickers)
        self.asset_def_box.hide()
        self.asset_def_box.dropdown_widget.currentTextChanged.connect(self.verify_inputs_validity)

        self.days_def_box = NumberSpinWidget("Forecast Days:", 1, 10, 1)
        self.days_def_box.hide()

        input_frame_layout.addWidget(self.analyze_type_def_box)
        input_frame_layout.addWidget(self.sector_def_box)
        input_frame_layout.addWidget(self.industry_def_box)
        input_frame_layout.addWidget(self.asset_def_box)
        input_frame_layout.addWidget(self.days_def_box)
        input_frame_layout.addWidget(self.start_button)

        self.input_frame.setLayout(input_frame_layout)
        ''''''

        '''Output side build'''
        self.output_frame = QFrame()
        self.input_frame.setFixedWidth(int(1280 * 0.3))
        output_frame_layout = QVBoxLayout()

        self.output_field = OutputTextEditWidget()
        self.output_field.setFixedHeight(int(720 * 0.3))

        self.plot_canvas_field = PlotCanvasWidget()
        self.plot_canvas_field.setFixedHeight(int(720 * 0.68))

        output_frame_layout.addWidget(self.output_field)
        output_frame_layout.addWidget(self.plot_canvas_field)

        self.output_frame.setLayout(output_frame_layout)
        ''''''

        layout.addWidget(self.input_frame)
        layout.addWidget(self.output_frame)
        self.setLayout(layout)

    def update_input_fields(self, index):
        if index == 0:
            self.sector_def_box.show()
            self.industry_def_box.hide()
            self.asset_def_box.hide()
            self.days_def_box.show()
        elif index == 1:
            self.sector_def_box.show()
            self.industry_def_box.show()
            self.asset_def_box.hide()
            self.days_def_box.show()
        elif index == 2:
            self.sector_def_box.hide()
            self.industry_def_box.hide()
            self.asset_def_box.show()
            self.days_def_box.show()
        else:
            self.sector_def_box.hide()
            self.industry_def_box.hide()
            self.asset_def_box.hide()
            self.days_def_box.hide()

    def update_by_sector(self, index, names_list):
        industry_names = self.data_provider.get_industry_names_by_sector(names_list[index])
        self.industry_def_box.update_options(industry_names)

    def verify_inputs_validity(self):
        type_index = self.analyze_type_def_box.dropdown_widget.currentIndex()
        if type_index == 0:
            self.sector_input_check()
        elif type_index == 1:
            self.sector_industry_input_check()
        elif type_index == 2:
            self.asset_input_check()
        else:
            self.start_button.setEnabled(False)

    def trigger_start(self):
        type_index = self.analyze_type_def_box.dropdown_widget.currentIndex()
        if type_index == 0:
            self.worker = Worker(self.analyze_sector_process)
        elif type_index == 1:
            self.worker = Worker(self.analyze_industry_process)
        elif type_index == 2:
            self.worker = Worker(self.analyze_asset_process)
        self.worker.signals.set_enabled.connect(self.start_button.setEnabled)
        self.worker.signals.update_output.connect(self.output_field.append)

        QThreadPool.globalInstance().start(self.worker)

    def sector_input_check(self):
        is_valid = self.sector_def_box.is_current_value_valid()

        if is_valid:
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def sector_industry_input_check(self):
        is_sector_valid = self.sector_def_box.is_current_value_valid()
        is_industry_valid = self.industry_def_box.is_current_value_valid()

        if is_sector_valid and is_industry_valid:
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def asset_input_check(self):
        is_valid = self.asset_def_box.is_current_value_valid()

        if is_valid:
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def analyze_sector_process(self):
        self.worker.signals.set_enabled.emit(False)
        sector_name = self.sector_def_box.get_current_value()
        n_days = self.days_def_box.get_value()

        start = datetime.now()
        self.worker.signals.update_output.emit(f"Started {sector_name} sector analysis.")

        results = forecast_for_sector(sector_name, n_days)
        aggregated_sector_results = aggregate_sector_forecast_results(results)

        actual_data = aggregated_sector_results[:-n_days]
        forecasts = aggregated_sector_results[-n_days:]

        self.worker.signals.update_output.emit(f"Forecasts for {sector_name}:")
        self.output_df(forecasts)
        self.plot_canvas_field.plot_forecasts(actual_data, forecasts)

        self.worker.signals.update_output.emit(f"Elapsed time: {datetime.now() - start}")
        self.worker.signals.set_enabled.emit(True)

    def analyze_industry_process(self):
        self.worker.signals.set_enabled.emit(False)
        industry_name = self.industry_def_box.get_current_value()
        n_days = self.days_def_box.get_value()

        start = datetime.now()
        self.worker.signals.update_output.emit(f"Started {industry_name} industry analysis.")

        results = forecast_for_industry(industry_name, n_days)
        aggregated_industry_results = aggregate_industry_forecast_results(results)

        actual_data = aggregated_industry_results[:-n_days]
        forecasts = aggregated_industry_results[-n_days:]

        self.worker.signals.update_output.emit(f"Forecasts for {industry_name}:")
        self.output_df(forecasts)
        self.plot_canvas_field.plot_forecasts(actual_data, forecasts)

        self.worker.signals.update_output.emit(f"Elapsed time: {datetime.now() - start}")
        self.worker.signals.set_enabled.emit(True)

    def analyze_asset_process(self):
        self.worker.signals.set_enabled.emit(False)
        company_name = self.asset_def_box.get_current_value()
        n_days = self.days_def_box.get_value()

        start = datetime.now()
        self.worker.signals.update_output.emit(f"Started {company_name} asset analysis")

        result = forecast_for_asset(company_name, n_days)
        result = result.pct_change().dropna()*100

        actual_data = result[:-n_days]
        forecasts = result[-n_days:]

        self.worker.signals.update_output.emit(f"Forecasts for {company_name}:")
        self.output_df(forecasts)
        self.plot_canvas_field.plot_forecasts(actual_data, forecasts)

        self.worker.signals.update_output.emit(f"Elapsed time: {datetime.now() - start}")
        self.worker.signals.set_enabled.emit(True)

    def output_df(self, data: pd.Series):
        for data_idx, value in data.items():
            date_str = data_idx.strftime('%Y-%m-%d')

            if value >= 0:
                value_text = f'<span style="color:green;">+{value:.4f}%</span>'
            else:
                value_text = f'<span style="color:red;">{value:.4f}%</span>'

            self.worker.signals.update_output.emit(f"{date_str}: {value_text}")


class GlobalFont(QFont):
    def __init__(self):
        super().__init__()

        self.setFamily('Cascadia Code')
        self.setPointSize(14)
