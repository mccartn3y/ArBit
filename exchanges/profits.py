import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Prices import AskAndBidGetter as aab 

class opp_finder():
    def __init__(self):
        a = aab()
        a.get_ask_and_bid_prices()
        #import data from exchanges and copy 
        self.exs = pd.read_csv('../exchanges.csv', index_col=0)
        df = self.exs[['Pay in', 'Pay out', 'Transaction']]
        df['Bid'] = pd.to_numeric(self.exs.Bid, errors='coerce')
        df['Ask'] = pd.to_numeric(self.exs.Ask, errors='coerce')
        
        #Calculate ETH from 100 EUR
        df['100EUR->ETH'] = ((100 - df['Pay in'] ) * (1-df['Transaction'])) / (df['Ask']-0.01)
        df['Out Ex'] = 'N/A'
        df['ETH->EUR'] = np.nan
        
        #Calculate ETH for every possible transaction
        df_copy = df.copy()
        for ex in df.index:
            temp_df = df_copy.copy()
            temp_df['Out Ex'] = ex
            temp_df['ETH->EUR'] = ((temp_df.loc[ex, '100EUR->ETH'] * (1-temp_df['Transaction'])) * (temp_df['Bid'] +0.01))-100
            df = df.append(temp_df)
            
        #Pivot results
        self.profits = df.pivot(columns='Out Ex', values='ETH->EUR')
        
    def plot_profits(self):
        sns.heatmap(self.profits)
        plt.show()

opp = opp_finder()
opp.plot_profits()
