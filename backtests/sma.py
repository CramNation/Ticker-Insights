import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import io
import base64

class SMAClass:
    
    def __init__(self, symbol):
    
        self.my_year_month_fmt = mdates.DateFormatter('%m/%y')
        self.symbol = symbol

        self.df_symbol_unfiltered = pd.read_json('https://api.iextrading.com/1.0/stock/'+self.symbol+'/chart/2y')
        self.df_symbol = self.df_symbol_unfiltered.dropna()

        self.df_symbol.set_index('date', inplace=True)

        self.closeprices = self.df_symbol['close']
        self.sma_20 = self.closeprices.rolling(window=20).mean()
        self.sma_50 = self.closeprices.rolling(window=50).mean()
        self.sma_100 = self.closeprices.rolling(window=100).mean()


    def plot(self):
        fig, ax = plt.subplots(figsize=(10,6))
        
        
        self.df_symbol['close'].plot(c='k',label='close prices')
        self.sma_20.plot(label='20 SMA')
        self.sma_50.plot(label='50 SMA')
        self.sma_100.plot(label='100 SMA')

        ax.xaxis.set_major_formatter(self.my_year_month_fmt)
        ax.legend(loc="best")
        plt.xlabel('Date')

        #Make graph a byte object to reference
        graph = io.BytesIO()
        plt.savefig(graph, format="png")

        graph_img = base64.b64encode(graph.getvalue())
        graph_context = graph_img.decode('utf8')

        
        plt.close()
        return graph_context