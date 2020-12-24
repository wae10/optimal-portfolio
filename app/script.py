import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as web
from matplotlib.ticker import FuncFormatter

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.cla import CLA
from pypfopt.plotting import plot_weights
from matplotlib.ticker import FuncFormatter
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from app.functions import plot_efficient_frontier
from collections import namedtuple

#NEW
from dotenv import load_dotenv
import os
from app import APP_ENV

# from __init__ import APP_ENV

def optimal_shares(tickers, start, end, amount):
    """Returns optimal llocation to individual assets to maximize sharpe ratio of portfolio

    Args:
        tickers (list): list of desired stock tickers
        start (string): starting date, yyyy-mm-dd
        end (string): ending date, yyyy-mm-dd
        amount (double): amount invested
    """

    if start is None or start == " ":
        start = '2015-01-01'
    if end is None or end == " ":
        end = '2020-06-06'

    #pt 1
    thelen = len(tickers)
    price_data = []
    for ticker in range(thelen):
        prices = web.DataReader(tickers[ticker], start=start, end = end, data_source='yahoo')
        price_data.append(prices.assign(ticker=ticker)[['Adj Close']])
        df_stocks = pd.concat(price_data, axis=1)
    df_stocks.columns=tickers

    #pt 2
    nullin_df = pd.DataFrame(df_stocks,columns=tickers)
    #print(nullin_df.isnull().sum())

    #pt 3
    #Annualized Return
    mu = expected_returns.mean_historical_return(df_stocks)

    #Sample Variance of Portfolio
    Sigma = risk_models.sample_cov(df_stocks)

    #pt 4
    #Max Sharpe Ratio - Tangent to the EF
    ef = EfficientFrontier(mu, Sigma, weight_bounds=(0,1)) #weight bounds in negative allows shorting of stocks
    sharpe_pfolio=ef.max_sharpe() #May use add objective to ensure minimum zero weighting to individual stocks
    sharpe_pwt=ef.clean_weights()
    # print("Optimal Weights (max sharpe ratio):",sharpe_pwt)

    #pt 5
    latest_prices = get_latest_prices(df_stocks)
    # Allocate Portfolio Value in $ as required to show number of shares/stocks to buy, also bounds for shorting will affect allocation
    #Min Volatility Portfolio Allocation $10000
    allocation, leftover = DiscreteAllocation(sharpe_pwt, latest_prices, total_portfolio_value=amount).lp_portfolio()
    print("Optimal shares to buy:", allocation)
    print("Leftover Fund value in $ after building maximum sharpe ratio portfolio is ${:.2f}".format(leftover))

    #performance = "calculates the expected return, volatility and Sharpe ratio for the optimised portfolio."
    performance = ef.portfolio_performance()

    return allocation, leftover, performance

def get_cla(tickers, start, end):
    """Returns CLA object for plot_efficient_frontier param as well as start / end dates

    Args:
        tickers (list): list of desired stock tickers
        start (string): starting date, yyyy-mm-dd
        end (string): ending date, yyyy-mm-dd
    """

    if start is None or start == " ":
        start = '2015-01-01'
    if end is None or end == " ":
        end = '2020-06-06'

    thelen = len(tickers)
    price_data = []
    for ticker in range(thelen):
        prices = web.DataReader(tickers[ticker], start=start, end = end, data_source='yahoo')
        price_data.append(prices.assign(ticker=ticker)[['Adj Close']])
        df_stocks = pd.concat(price_data, axis=1)
    df_stocks.columns=tickers

    #pt 2
    nullin_df = pd.DataFrame(df_stocks,columns=tickers)
    #print(nullin_df.isnull().sum())

    #pt 3
    #Annualized Return
    mu = expected_returns.mean_historical_return(df_stocks)

    #Sample Variance of Portfolio
    Sigma = risk_models.sample_cov(df_stocks)

    cla = CLA(mu, Sigma, weight_bounds=(-1,1))

    return cla, start, end

def graph_closes(tickers, start, end):
    """Graphs stacked daily closed for all stocks

    Args:
        tickers (list): list of desired stock tickers
        start (string): starting date, yyyy-mm-dd
        end (string): ending date, yyyy-mm-dd
    """

    if start is None or start == " ":
        start = '2015-01-01'
    if end is None or end == " ":
        end = '2020-06-06'

    thelen = len(tickers)
    price_data = []
    for ticker in range(thelen):
        prices = web.DataReader(tickers[ticker], start=start, end =end, data_source='yahoo')
        price_data.append(prices.assign(ticker=ticker)[['Adj Close']])
        df_stocks = pd.concat(price_data, axis=1)
    df_stocks.columns=tickers

    #pt 2
    nullin_df = pd.DataFrame(df_stocks,columns=tickers)
    #print(nullin_df.isnull().sum())


    # Create the title 'Portfolio Adj Close Price History
    title = 'Portfolio Adj. Close Price History    '
    #Get the stocks
    my_stocks = nullin_df
    #Create and plot the graph
    plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
    # Loop through each stock and plot the Adj Close for each day
    for c in my_stocks.columns.values:
        plt.plot( my_stocks[c],  label=c)#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
    plt.title(title)
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Adj. Price USD ($)',fontsize=18)
    plt.legend(my_stocks.columns.values, loc='upper left')
    plt.show()

def graph_weights(tickers, start, end):
    """Displays bar chart of optimal weights to maximize portfolio sharpe ratio

    Args:
        tickers (list): list of desired stock tickers
        start (string): starting date, yyyy-mm-dd
        end (string): ending date, yyyy-mm-dd
    """

    if start is None or start == " ":
        start = '2015-01-01'
    if end is None or end == " ":
        end = '2020-06-06'

    thelen = len(tickers)
    price_data = []
    for ticker in range(thelen):
        prices = web.DataReader(tickers[ticker], start=start, end = end, data_source='yahoo')
        price_data.append(prices.assign(ticker=ticker)[['Adj Close']])
        df_stocks = pd.concat(price_data, axis=1)
    df_stocks.columns=tickers

    #pt 2
    nullin_df = pd.DataFrame(df_stocks,columns=tickers)
    #print(nullin_df.isnull().sum())

    #pt 3
    #Annualized Return
    mu = expected_returns.mean_historical_return(df_stocks)

    #Sample Variance of Portfolio
    Sigma = risk_models.sample_cov(df_stocks)

    #pt 4
    #Max Sharpe Ratio - Tangent to the EF
    ef = EfficientFrontier(mu, Sigma, weight_bounds=(0,1)) #weight bounds in negative allows shorting of stocks
    sharpe_pfolio=ef.max_sharpe() #May use add objective to ensure minimum zero weighting to individual stocks
    sharpe_pwt=ef.clean_weights()
    # print("Optimal Weights (max sharpe ratio):",sharpe_pwt)

    plot_weights(sharpe_pwt)

def print_menu():
    print("\n")
    print(30 * "-" , "MENU" , 30 * "-")
    print("1. Optimal Shares")
    print("2. Graph Efficient Portfolio")
    print("3. Graph Closing Prices")
    print("4. Graph Optimal Weights")
    print("5. Exit")
    print(67 * "-")
  
def menu():
    """Displays menu of options to choose from. Lists all functions
    """ 
    loop=True   

    tickers = []
    go = True
    while go:
        ticker = input("Enter ticker (enter 'stop' when done):\n")
        if ticker.upper() == "STOP":
            go = False
        else:
            tickers.append(ticker)

    start = input("\nEnter start date (yyyy-mm-dd) or space + enter for default: ")
    end = input("\nEnter end date (yyyy-mm-dd) or space + enter for default: ")
        

    while loop:          ## While loop which will keep going until loop = False
        print_menu()    ## Displays menu
        choice = eval(input("Enter your choice [1-5]: "))
        
        if choice==1:
            amount = eval(input("Enter amount you want to invest (format as number): "))     
            allocation, leftover, performance = optimal_shares(tickers, start, end, amount)

        elif choice==2:
            cla, start, end = get_cla(tickers,start,end)
            plot_efficient_(cla, start, end, points=100, show_assets=True)

        elif choice==3:
            graph_closes(tickers,start,end)

        elif choice==4:
            graph_weights(tickers,start,end)

        elif choice==5:
            loop=False # This will make the while loop to end as not value of loop is set to False

        else:
            # Any integer inputs other than values 1-5 we print an error message
            print("Wrong option selection. Enter any key to try again..")

def main():
    menu()

if __name__ == "__main__":
    if APP_ENV == "development":

        main()