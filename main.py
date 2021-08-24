# This is a sample Python script.
import yfinance as yf
import pandas as pd


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def get_stock_info(name):
    # Use a breakpoint in the code line below to debug your script.
    stock = yf.Ticker(name)
    return stock.history(period="3y")


# Press the green button in the gutter to run the script.
def calculate_dollar_cost(df_stock_info, amount):
    total_amount = 0
    total_shares = 0
    days_count = 0

    total_dividant = 0
    divident = 0

    for index, row in df_stock_info.iterrows():
        closed = row['Close']
        share = amount / closed
        total_amount += amount
        total_shares += share
        if row['Dividends'] != 0:
            divident += (total_shares * row['Dividends'])
            total_dividant += divident

        days_count += 1

    print("total_dividant", round(total_dividant,2))
    print("total_amount", round(total_amount,2))
    print("total_shares", round(total_shares,2))
    print("days_count", days_count)

    return total_amount, total_shares, days_count


def calculate_consecutive_low(df_stock_info, amount, dailyInvest):
    price_2_days_back = 0
    price_1_days_back = 0
    amount_invested = 0
    total_shares = 0
    days_count = 0
    collective_amount = 0

    for index in range(len(df_stock_info)):

        closed = df_stock_info.loc[index, 'Open']
        if closed < price_1_days_back < price_2_days_back:
            days_count += 1
            share = (collective_amount + dailyInvest) / closed
            amount_invested += (collective_amount + dailyInvest)
            total_shares += share
            collective_amount = 0
            price_2_days_back = 0
            price_1_days_back = 0
        else:
            share = dailyInvest / closed
            collective_amount += (amount - dailyInvest)
            amount_invested += dailyInvest
            total_shares += share
            days_count += 1

        price_2_days_back = price_1_days_back
        price_1_days_back = closed

    print("total_amount for two low", amount_invested)
    print("total_shares for two low", total_shares)
    print("days_count for two low", days_count)
    print("==========================")

    return amount_invested, total_shares, days_count


def divident_reinvestment(df_stock_info, amount):
    total_amount = 0
    total_shares = 0
    days_count = 0
    total_dividant = 0
    divident = 0
    for index, row in df_stock_info.iterrows():
        closed = row['Close']
        share = amount / closed
        total_amount += amount
        total_shares += share
        if row['Dividends'] != 0:
            divident += (total_shares * row['Dividends'])
            total_dividant += divident
            share2 = divident / closed
            total_amount += divident
            total_shares += share2
        days_count += 1

    print("total_dividant", round(total_dividant,2))
    print("total_amount divident_reinvestment", round(total_amount,2))
    print("total_shares divident_reinvestment", round(total_shares,2))
    print("days_count divident_reinvestment", days_count)

    return total_amount, total_shares, days_count


def calculate_profit(total_amount_invested, total_shares, closed_price):
    profit = round(closed_price * total_shares - total_amount_invested,2)
    print("profit ", profit)
    print("============== ")
    return profit, get_change(closed_price * total_shares, total_amount_invested )


def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')

if __name__ == '__main__':
    df_stock_info = get_stock_info('SCHD')
    print(df_stock_info.columns)
    # Convert the dictionary into DataFrame
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df = pd.DataFrame(df_stock_info, columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
    df.reset_index(inplace=True)

    print("calculate_dollar_cost ")
    total_amount_invested, total_shares, days_count = calculate_dollar_cost(df, 15)
    profit, percent_change = calculate_profit(total_amount_invested, total_shares, df['Close'].iloc[-1])

    print("divident_reinvestment")
    total_amount, total_shares, days_count = divident_reinvestment(df, 15)
    profit1, percent_change2 = calculate_profit(total_amount_invested, total_shares, df['Close'].iloc[-1])

    print("percent_change direct ", get_change(df['Close'].iloc[-1], df['Close'].iloc[0]))

    print("percent_change ", percent_change)
    print("percent_change ", percent_change2)


    print("difference ", round(profit1 - profit, 2))