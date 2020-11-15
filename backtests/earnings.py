import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
import base64


class EarningsClass:

    def __init__(self, symbol):
        
        #Initialize symbol
        self.symbol = symbol
        
        #Request data from API and drop null
        self.df_symbol_unfiltered = pd.read_json('https://api.iextrading.com/1.0/stock/'+self.symbol+'/chart/1y')
        self.df_symbol = self.df_symbol_unfiltered.dropna()
        
        #Request earnings data from API 
        self.df_earnings_unfiltered = pd.read_json('https://api.iextrading.com/1.0/stock/'+self.symbol+'/earnings')
        
        #Make earnings data into an itterable list then back into a formatted dataframe
        self.df_symbol.set_index('date', inplace=True)
        self.earnings_list_data = self.df_earnings_unfiltered['earnings'].tolist()
        self.df_new_earnings = pd.DataFrame(self.earnings_list_data, columns=['EPSReportDate', 'actualEPS', 'consensusEPS', 'estimatedEPS', 'announceTime', 'numberOfEstimates','EPSSurpriseDollar', 'fiscalPeriod', 'fiscalEndDate', 'yearAgo', 'yearAgoChangePercent', 'estimatedChangePercent', 'symbolId'], index=['Q4', 'Q3', 'Q2', 'Q1'])
        
        #Make NaN values a string
        self.df_earnings = self.df_new_earnings.replace(np.nan, ("an unknown value"))
        
        # Find discrepancy between Actual and Estimated
        self.df_EPSSurpriseDollar = self.df_earnings['EPSSurpriseDollar']

        #Make variables for the discrepancies
        self.Q1_diff = (self.df_EPSSurpriseDollar[3])
        self.Q2_diff = (self.df_EPSSurpriseDollar[2])
        self.Q3_diff = (self.df_EPSSurpriseDollar[1])
        self.Q4_diff = (self.df_EPSSurpriseDollar[0])
        
        #Make dates an itterable list
        self.symbol_report_dates = self.df_earnings['EPSReportDate'].values.tolist()

        #Find earning report date 
        self.Q1_date = (self.symbol_report_dates[3])
        self.Q2_date = (self.symbol_report_dates[2])
        self.Q3_date = (self.symbol_report_dates[1])
        self.Q4_date = (self.symbol_report_dates[0])

        #Format dates into year-month-day (for plot)
        self.Q1_datetime = datetime.strptime(self.Q1_date, '%Y-%m-%d')
        self.Q2_datetime = datetime.strptime(self.Q2_date, '%Y-%m-%d')
        self.Q3_datetime = datetime.strptime(self.Q3_date, '%Y-%m-%d')
        self.Q4_datetime = datetime.strptime(self.Q4_date, '%Y-%m-%d')
        
        #Format dates into day-month-year (for text)
        self.Q1_readable_date = datetime.strptime(self.Q1_date, '%Y-%m-%d').strftime('%m/%d/%y')
        self.Q2_readable_date = datetime.strptime(self.Q2_date, '%Y-%m-%d').strftime('%m/%d/%y')
        self.Q3_readable_date = datetime.strptime(self.Q3_date, '%Y-%m-%d').strftime('%m/%d/%y')
        self.Q4_readable_date = datetime.strptime(self.Q4_date, '%Y-%m-%d').strftime('%m/%d/%y')
           
        #Start date period for plot
        self.Q1_start_date = self.Q1_datetime - timedelta(days=10)
        self.Q2_start_date = self.Q2_datetime - timedelta(days=10)
        self.Q3_start_date = self.Q3_datetime - timedelta(days=10)
        self.Q4_start_date = self.Q4_datetime - timedelta(days=10)
        
        #End date period for plot
        self.Q1_end_date = self.Q1_datetime + timedelta(days=10)
        self.Q2_end_date = self.Q2_datetime + timedelta(days=10)
        self.Q3_end_date = self.Q3_datetime + timedelta(days=10)
        self.Q4_end_date = self.Q4_datetime + timedelta(days=10)
        
    
    def Q1_string(self):
        
        if self.Q1_diff != "an unknown value":
             
            if self.Q1_diff > 0:
                return(self.symbol.upper() + " beat Q1 earnings by " + str(self.Q1_diff) + " on " + str(self.Q1_readable_date))
            elif self.Q1_diff < 0:
                return(self.symbol.upper() + " missed Q1 earnings by " + str(self.Q1_diff) + " on " + str(self.Q1_readable_date))
        else:
            return('We do not have data for ' + self.symbol.upper() + ' Q1 earnings on ' + str(self.Q1_readable_date))
    
    def Q2_string(self):
        
        if self.Q2_diff != "an unknown value":
            
            if self.Q2_diff > 0:
                return(self.symbol.upper() + " beat Q2 earnings by " + str(self.Q2_diff) + " on " + str(self.Q2_readable_date))
            elif self.Q2_diff < 0:
                return(self.symbol.upper() + " missed Q2 earnings by " + str(self.Q2_diff) + " on " + str(self.Q2_readable_date))
        else:
            return('We do not have data for ' + self.symbol.upper() + ' Q2 earnings on ' + str(self.Q2_readable_date))
            
    def Q3_string(self):
        if self.Q3_diff != "an unknown value":
            
            if self.Q3_diff > 0:
                return(self.symbol.upper() + " beat Q3 earnings by " + str(self.Q3_diff) + " on " + str(self.Q3_readable_date))
            elif self.Q4_diff < 0:
                return(self.symbol.upper() + " missed Q3 earnings by " + str(self.Q3_diff) + " on " + str(self.Q3_readable_date))
        else:
            return('We do not have data for ' + self.symbol.upper() + ' Q3 earnings on ' + str(self.Q3_readable_date))
            
    def Q4_string(self):
        if self.Q4_diff != "an unknown value":
        
            if self.Q4_diff > 0:
                return(self.symbol.upper() + " beat Q4 earnings by " + str(self.Q4_diff) + " on " + str(self.Q4_readable_date))
            elif self.Q4_diff < 0:
                return(self.symbol.upper() + " missed Q4 earnings by " + str(self.Q4_diff) + " on " + str(self.Q4_readable_date))
        else:
            return('We do not have data for ' + self.symbol.upper() + ' Q4 earnings on ' + str(self.Q4_readable_date))
            
    def Q1_plot(self):
        self.df_symbol['close'][self.Q1_start_date : self.Q1_end_date].plot(figsize=(4,3), c='k', title= 'Q1 Earnings')
        plt.axvline(x=self.Q1_date, ls='--', c='r')
        plt.xlabel("")

        #Make graph a byte object to reference
        graph = io.BytesIO()
        plt.savefig(graph, format="png")

        graph_img = base64.b64encode(graph.getvalue())
        graph_context = graph_img.decode('utf8')

        
        plt.close()
        return graph_context

    def Q2_plot(self):
        self.df_symbol['close'][self.Q2_start_date : self.Q2_end_date].plot(figsize=(4,3), c='k', title= 'Q2 Earnings')
        plt.axvline(x=self.Q2_date, ls='--', c='r')
        plt.xlabel("")

        #Make graph a byte object to reference
        graph = io.BytesIO()
        plt.savefig(graph, format="png")

        graph_img = base64.b64encode(graph.getvalue())
        graph_context = graph_img.decode('utf8')

        
        plt.close()
        return graph_context
    
    def Q3_plot(self):
        self.df_symbol['close'][self.Q3_start_date : self.Q3_end_date].plot(figsize=(4,3), c='k', title= 'Q3 Earnings')
        plt.axvline(x=self.Q3_date, ls='--', c='r')
        plt.xlabel("")

        #Make graph a byte object to reference
        graph = io.BytesIO()
        plt.savefig(graph, format="png")

        graph_img = base64.b64encode(graph.getvalue())
        graph_context = graph_img.decode('utf8')

        
        plt.close()
        return graph_context
    
    def Q4_plot(self):
        self.df_symbol['close'][self.Q4_start_date : self.Q4_end_date].plot(figsize=(4,3), c='k', title='Q4 Earnings')
        plt.axvline(x=self.Q4_date, ls='--', c='r')
        plt.xlabel("")

        #Make graph a byte object to reference
        graph = io.BytesIO()
        plt.savefig(graph, format="png")

        graph_img = base64.b64encode(graph.getvalue())
        graph_context = graph_img.decode('utf8')

        
        plt.close()
        return graph_context