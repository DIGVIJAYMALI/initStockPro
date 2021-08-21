# Basic Py
'''
https://finance.yahoo.com/quote/VTI/
'''
import yfinance as yf
import pandas as pd

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def get_stock_info(name):
    # Use a breakpoint in the code line below to debug your script.
    stock = yf.Ticker(name)
    return stock.history(period="1y")


# Press the green button in the gutter to run the script.
def calculate_dollar_cost(df_stock_info, amount):
    total_amount = 0
    total_shares = 0
    days_count = 0
    for index, row in df_stock_info.iterrows():
        closed = row['Close']
        share = amount / closed
        total_amount += amount
        total_shares += share
        days_count +=1

    return total_amount, total_shares, days_count


def calculate_consecutive_low(df_stock_info, amount, dailyInvest):

    price_2_days_back = 0
    price_1_days_back = 0
    amount_invested = 0
    total_shares = 0
    days_count = 0
    collective_amount = 0
    for index in range(len(df_stock_info)):
        #if index == 0:
        #    price_2_days_back = df_stock_info.loc[index, 'Close']
        #    days_count += 1
        #    continue
        #if index == 1:
        #    price_1_days_back = df_stock_info.loc[index, 'Close']
        #    days_count += 1
        #    continue

        closed = df_stock_info.loc[index, 'Close']
        if closed < price_1_days_back < price_2_days_back:
            days_count += 1
            share = (collective_amount+dailyInvest) / closed
            amount_invested += (collective_amount+dailyInvest)
            total_shares += share
            collective_amount = 0
            price_2_days_back = 0
            price_1_days_back = 0
        else:
            share = dailyInvest / closed
            collective_amount += ( amount - dailyInvest)
            amount_invested += dailyInvest
            total_shares += share
            days_count += 1

        price_2_days_back = price_1_days_back
        price_1_days_back = closed

    return total_amount, total_shares, days_count


if __name__ == '__main__':
    print("start")
    df_stock_info = get_stock_info('VTI')
    print(df_stock_info.columns)
    # Convert the dictionary into DataFrame
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df = pd.DataFrame(df_stock_info, columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
    df.reset_index(inplace=True)

    total_amount, total_shares, days_count = calculate_dollar_cost(df, 15)

    print("total_amount", total_amount)
    print("total_shares", total_shares)
    print("days_count", days_count)

    total_amount1, total_shares1, days_count1 = calculate_consecutive_low(df, 15, 0)
    print("total_amount for two low", total_amount1)
    print("total_shares for two low", total_shares1)
    print("days_count for two low", days_count1)