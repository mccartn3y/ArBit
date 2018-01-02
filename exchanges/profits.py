import pandas as pd
import numpy as np
import matplotlib as mlp
mlp.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from Prices import AskAndBidGetter as aab
import datetime

class opp_finder():
    def __init__(self):
        #Update exchanges file
        try:
            a = aab()
            a.get_ask_and_bid_prices()
        except Exception as ex:
            print(str(type(ex))+": Exchange database not updated")
        time = datetime.datetime.now().isoformat()
        #import data from exchanges and copy 
        self.exs = pd.read_csv('../exchanges.csv', index_col=0)
        df = self.exs[['Pay in', 'Pay out', 'Transaction']]
        df['Bid'] = pd.to_numeric(self.exs.Bid, errors='coerce')
        df['Ask'] = pd.to_numeric(self.exs.Ask, errors='coerce')
        df['Date'] = time
        
        #Calculate ETH from 100 EUR
        df['100EUR->ETH'] = ((5 - df['Pay in'] ) * (1-df['Transaction'])) / (df['Ask']-0.01)
        df['Out Ex'] = 'N/A'
        df['ETH->EUR'] = np.nan
        
        #Calculate ETH for every possible transaction
        df_copy = df.copy()
        for ex in df.index:
            temp_df = df_copy.copy()
            temp_df['Out Ex'] = ex
            temp_df['ETH->EUR'] = (((temp_df['100EUR->ETH']
                                     * (1-temp_df.loc[ex, 'Transaction']))
                                    * (temp_df.loc[ex, 'Bid'] +0.01))
                                   -temp_df.loc[ex, 'Pay out'])-5
            #print(temp_df[['100EUR->ETH', 'Out Ex', 'ETH->EUR']])
            df = df.append(temp_df)

        self.df = df
            
        #Pivot results
        self.profits = df.pivot(columns='Out Ex', values='ETH->EUR')
        print(self.profits)
        
    def plot_profits(self):
        sns.heatmap(self.profits)
        plt.show()

    def df_to_SQL(self, connection):
        self.df.to_sql("ArBit_history", connection, index_label='In Ex')

    def top_trades(self, n):
        temp = self.df.sort_values('ETH->EUR', ascending=False)
        return temp.iloc[:n, :]

opp = opp_finder()
print(opp.top_trades(5))
