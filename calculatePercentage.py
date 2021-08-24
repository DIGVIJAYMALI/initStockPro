# This is a sample Python script.
import yfinance as yf
import pandas as pd


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def get_stock_info(name):
    # Use a breakpoint in the code line below to debug your script.
    stock = yf.Ticker(name)
    return stock.history(period="1y")


def calculate_percentage_change_in_one_year(name):
    df_stock_info = get_stock_info(name)
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df = pd.DataFrame(df_stock_info, columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
    last_closed = df['Close'].iloc[-1]
    year_before_closed = df['Close'].iloc[0]
    return get_change(last_closed, year_before_closed)

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')

if __name__ == '__main__':

    companylst = ['MSFT', 'AAPL', 'DIS','GOOGL','TSLA','NVDA','AMD','JNJ', 'NKE','AMZN']
    dframe = pd.DataFrame(companylst)
    percent_change_list = []
    for name in companylst:
        print("for ", name)
        percent_changed = calculate_percentage_change_in_one_year(name)
        print("% change ", percent_changed)
        percent_change_list.append(percent_changed)

    percentile_list = pd.DataFrame(
        {'companies': companylst,
         '% change': percent_change_list,
         })

    print("final list ", percentile_list)
