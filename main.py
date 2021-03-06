# This is a sample Python script.
import yfinance as yf
import pandas as pd
import numpy as np
import math as math

def get_stock_info(name):
    # Use a breakpoint in the code line below to debug your script.
    stock = yf.Ticker(name)
    return stock.history(period="1y")

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')

# Press the green button in the gutter to run the script.
def calculate_dollar_cost_with_min_average_new(df_stock_info, amount, is_dividant):
    total_amount = 0
    total_shares = 0
    days_count = 0
    days_uninvested = 0
    days_not_invested = 0
    df_stock_info.index = np.arange(1, len(df) + 1)
    weekly_budget = amount * 5
    divident = 0
    total_dividant = 0
    count =1
    five_day_stock = 0
    five_day_amount = 0

    for index, row in df_stock_info.iterrows():
        closed = round(row['Close'],2)
        five_day_avg = row['5_day_avg']

        if row['Dividends'] != 0 and is_dividant:
            divident += (total_shares * row['Dividends'])
            total_dividant += divident
            share2 = divident / closed
            count+=1
            total_shares += share2

        if math.isnan(row['5_day_avg']):
            share = amount / closed
            total_amount += amount
            total_shares += share
            five_day_stock += share
            five_day_amount += amount
            days_count += 1
            weekly_budget -= amount
            days_uninvested = 0
            continue

        if index % 5 == 0:
            if weekly_budget > 0:
                share = (weekly_budget) / closed
                total_amount += (weekly_budget)
                total_shares += share
                days_count += (weekly_budget/amount)
                days_uninvested = 0
            five_day_stock = 0
            five_day_amount = 0
            weekly_budget = amount * 5

        our_five_day_avg = 0
        if five_day_stock != 0:
            our_five_day_avg = five_day_amount / five_day_stock

        if closed > (our_five_day_avg * 1.12):
            days_uninvested += 1
            days_not_invested+= 1
            continue
        elif weekly_budget > 0:
            share = amount / closed
            total_amount += amount
            total_shares += share

            five_day_stock += share
            five_day_amount += amount
            weekly_budget -= amount
            days_count += 1

            if closed < our_five_day_avg * 0.8 and weekly_budget > 0:
                share = (weekly_budget) / closed
                total_amount += (weekly_budget)
                total_shares += share
                days_count += (weekly_budget/amount)
                weekly_budget = 0
                days_uninvested = 0

    print("total_dividant", round(total_dividant, 2))
    print("total_amount", round(total_amount, 2))
    print("total_shares", round(total_shares, 2))
    print("days_count", days_count)
    print("days_not_invested", days_not_invested)
    print("Price per share ", total_amount / total_shares)
    print("==========================")

    return total_amount, total_shares, days_count

# Press the green button in the gutter to run the script.
def calculate_dollar_cost_with_min_average2(df_stock_info, amount):
    total_amount = 0
    total_shares = 0
    days_count = 0
    monthly_budget = amount * 20
    days_uninvested = 0

    df_stock_info.index = np.arange(1, len(df) + 1)

    for index, row in df_stock_info.iterrows():
        closed = row['Close']
        five_day_avg = row['5_day_avg']
        if index == 1:
            share = amount / closed
            total_amount += amount
            monthly_budget -= amount
            total_shares += share
            days_count+=1
            #print(row['Date'])
            continue
        if index % 20 == 0 and monthly_budget > 0:
            share = monthly_budget / closed
            total_amount += monthly_budget
            monthly_budget -= monthly_budget
            total_shares += share
            days_count += 1
            #print(row['Date'])
            continue
        if index % 20 == 0:
            monthly_budget = amount * 20

        if days_uninvested == 5:
             share = (amount * days_uninvested) / closed
             total_amount += (amount * days_uninvested)
             total_shares += share
             monthly_budget -= (amount * days_uninvested)
             days_uninvested = 0
             days_count += 5

        if math.isnan(row['5_day_avg']):
            share = amount / closed
            total_amount += amount
            monthly_budget -= amount
            total_shares += share
            days_count += 1
            continue
        if closed > (row['5_day_avg']):
            days_uninvested += 1
            continue
        if closed < (row['5_day_avg']) and monthly_budget > 0:
            if days_uninvested == 0:
                days_uninvested = 1

            share = (amount*days_uninvested) / closed
            total_amount += (amount*days_uninvested)
            total_shares += share
            monthly_budget-= (amount*days_uninvested)
            days_count += days_uninvested
            days_uninvested = 0



    print("total_amount", round(total_amount, 2))
    print("total_shares", round(total_shares, 2))
    print("days_count", days_count)
    print("Price per share ", (total_amount) / total_shares)
    print("==========================")

    return total_amount, total_shares, days_count

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
    print("Price per share ", total_amount/total_shares)
    print("==========================")
    return total_amount, total_shares, days_count

# Press the green button in the gutter to run the script.
def calculate_dollar_cost_with_min_average(df_stock_info, amount):
    total_amount = 0
    total_shares = 0
    days_count = 0
    total_dividant = 0
    divident = 0
    days_uninvested = 0
    monthly_budget = amount*20

    for index, row in df_stock_info.iterrows():
        closed = row['Close']
        if days_count == 0:
            share = amount / closed
            total_amount += amount
            monthly_budget -= amount
            total_shares += share
            days_uninvested +=1
        else:
            if days_uninvested == 20:
                share = (amount*20) / closed
                total_amount += amount*20
                monthly_budget -= (amount*20)
                total_shares += share
                days_uninvested = 1
                monthly_budget = amount * 20
            else:
                average_cost = total_amount/total_shares
                if closed < (average_cost * 1.02):
                    share = (amount*days_uninvested) / closed
                    total_amount += (amount*days_uninvested)
                    total_shares += share
                    days_uninvested = 1
                if closed <= average_cost:
                    share = amount / closed
                    total_amount += amount
                    monthly_budget -= amount
                    total_shares += share
                    days_uninvested = 1
                if closed > average_cost * 1.02:
                    days_uninvested += 1
        if days_count % 20 == 0:
            if monthly_budget > 0 :
                share = (monthly_budget) / closed
                total_amount += (monthly_budget)
                total_shares += share
                days_uninvested = 1
            monthly_budget = amount*20
        if row['Dividends'] != 0:
            divident += (total_shares * row['Dividends'])
            total_dividant += divident
        days_count += 1

    print("uninvested amount ", round(monthly_budget, 2))
    print("total_dividant", round(total_dividant,2))
    print("total_amount", round(total_amount,2))
    print("total_shares", round(total_shares,2))
    print("days_count", days_count)
    print("Price per share ", total_amount/total_shares)

    print("final total amount ", round(monthly_budget + total_amount, 2))
    print("==========================")
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
    print("Price per share ", amount_invested/total_shares )
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
            #total_amount += divident
            total_shares += share2
        days_count += 1

    print("total_dividant", round(total_dividant,2))
    print("total_amount divident_reinvestment", round(total_amount,2))
    print("total_shares divident_reinvestment", round(total_shares,2))
    print("days_count divident_reinvestment", days_count)
    print("Price per share ", total_amount/total_shares )
    return total_amount, total_shares, days_count


def calculate_profit(total_amount_invested, total_shares, closed_price):
    profit = round(closed_price * total_shares - total_amount_invested,2)
    percent_change_amount = get_change(closed_price * total_shares, total_amount_invested)

    print("profit ", profit)
    print("percent_change_amount ", percent_change_amount)
    print("============== ")

    return profit, get_change(closed_price * total_shares, total_amount_invested )


def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')


Input_column = {
    "ID": int,
    "Name": str,
    "Address": str
}


if __name__ == '__main__':
    df_stock_info = get_stock_info('VTI')
    amount = 5
    #print(df_stock_info.columns)
    print(df_stock_info)

    # Convert the dictionary into DataFrame
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df = pd.DataFrame(df_stock_info, columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])


    df['5_day_avg'] = round(df.Close.rolling(window=5).mean(), 2)
    df['closed_p_change'] = df.Close.pct_change(periods=1)

    max_value = df.closed_p_change.max()
    min_value = df.closed_p_change.min()
    mean_value = df.closed_p_change.mean()
    print(f"max value {max_value}")
    print(f"min value {min_value}")
    print(f"mean value {mean_value}")

    #df.to_csv("vti_10y.csv")

    print("last price")
    print(df['Close'].iloc[-1])

    #print("calculate_dollar_cost ")
    #total_amount_invested, total_shares, days_count = calculate_dollar_cost(df, amount)
    #profit, percent_change = calculate_profit(total_amount_invested, total_shares, df['Close'].iloc[-1])

    #print("calculate_dollar_cost_with_min_average ")
    #total_amount_invested, total_shares, days_count = calculate_dollar_cost_with_min_average_new(df, amount, True)
    #profit, percent_change = calculate_profit(total_amount_invested, total_shares, df['Close'].iloc[-1])

    print("============== ")
    print("divident_reinvestment")
    print("============== ")
    total_amount, total_shares, days_count = divident_reinvestment(df, amount)
    print("============== ")
    profit1, percent_change2 = calculate_profit(total_amount, total_shares, df['Close'].iloc[-1])

    #print("percent_change direct ", get_change(df['Close'].iloc[-1], df['Close'].iloc[0]))

    #print("percent_change ", percent_change)
    #print("percent_change ", percent_change2)
    #print("calculate_consecutive_low ")
    #total_amount_invested, total_shares, days_count = calculate_consecutive_low(df, 15, 0)


    #print("difference ", round(profit1 - profit, 2))