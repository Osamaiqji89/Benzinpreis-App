import os
import pandas as pd
import traceback
import zipfile
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from services.FuelPriceDB import FuelPriceDB
from utils.StatusLogger import StatusLogger

class History:
    def __init__(self, grid_layout_history):
        try:
            self.grid_layout_history = grid_layout_history
            self.fuelPriceDB = FuelPriceDB()
            self.historical_data = self.fuelPriceDB.get_all_prices()
            self.plot_widget = QWidget()
            self.plot_layout = QVBoxLayout(self.plot_widget)
            self.figure = Figure(figsize=(10, 6))
            self.canvas = FigureCanvas(self.figure)
            self.plot_layout.addWidget(self.canvas)
            self.grid_layout_history.addWidget(self.plot_widget)
            StatusLogger.log("Initializing History module")
        except Exception as e:
            StatusLogger.error(f"Error initializing History: {e}")
            raise

    def create_price_history_plot(self, fuel_type):
        try:
            self.figure.clear()

            if fuel_type not in self.historical_data:
                self._draw_message('Keine historischen Daten verfügbar für diesen Kraftstofftyp')
                return

            ax = self.figure.add_subplot(111)
            self._configure_plot_style(ax)

            years = list(self.historical_data[fuel_type].keys())
            months = range(1, 13)

            for year in years:
                prices = self.historical_data[fuel_type][year]
                ax.plot(months, prices, marker='o', label=year)

            ax.set_xlabel('Monat', color='#616161')
            ax.set_ylabel('Durchschnittspreis (€)', color='#616161')
            ax.set_title(f'Preisentwicklung für {fuel_type.upper()} - Letzte Jahre', color='#616161')
            ax.set_xticks(months)
            ax.set_xticklabels(['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'],
                               rotation=45, ha='right', color='#616161')
            ax.legend(title='Jahr', loc='upper right', facecolor='#fbfce2', edgecolor='#616161', labelcolor='#616161')

            self.figure.tight_layout()
            self.canvas.draw()

            StatusLogger.success("Price history plot created")
        except Exception as e:
            StatusLogger.error(f"Error creating price history plot: {e}")
            traceback.print_exc()

    def plot_price_trend(self, prices_df, fuel_type, plz_prefix):
        try:
            prices_df['date'] = pd.to_datetime(prices_df['date'])
            daily_prices = prices_df.groupby(prices_df['date'].dt.date)[fuel_type].mean().reset_index()

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self._configure_plot_style(ax)

            ax.plot(daily_prices['date'], daily_prices[fuel_type], marker='o')

            ax.set_xlabel('Datum', color='#616161')
            ax.set_ylabel('Preis (€)', color='#616161')
            ax.set_title(f'Preisentwicklung für {fuel_type.upper()} - PLZ-Region {plz_prefix}', color='#616161')
            ax.tick_params(axis='x', rotation=45)

            self.figure.tight_layout()
            self.canvas.draw()

            StatusLogger.success("Price trend plot created")
        except Exception as e:
            StatusLogger.error(f"Error plotting price trend: {e}")
            traceback.print_exc()
            self._draw_message('Fehler beim Erstellen des Preistrends')

    def _configure_plot_style(self, ax):
        self.figure.patch.set_facecolor('#e3e4d0')
        ax.set_facecolor('#e3e4d0')
        ax.grid(True)
        ax.tick_params(axis='y', colors='#616161')
        ax.tick_params(axis='x', colors='#616161')
        for spine in ax.spines.values():
            spine.set_color('#616161')

    def _draw_message(self, message):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, message, horizontalalignment='center', verticalalignment='center')
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvas.draw()
