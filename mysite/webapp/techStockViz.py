import datetime
import plotly.offline as py
import plotly.graph_objs as gp
import pandas_datareader as web

class TechStock:

    def __init__(self, stockSym, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.stockSym = stockSym

    def getTechStock(self):
        stockDf = web.DataReader(self.stockSym, 'yahoo', self.startDate, self.endDate)
        #TWTR = web.DataReader('TWTR', 'yahoo', self.start, self.end)
        #AAPL = web.DataReader('AAPL', 'yahoo', self.start, self.end)
        print("##$#$#$#$#:",stockDf.info())
        trace1 = gp.Ohlc(
            x = stockDf.index[:],
            open = stockDf['Open'],
            high = stockDf['High'],
            low = stockDf['Low'],
            close = stockDf['Close'],
            name = self.stockSym,
            increasing = dict(line = dict(color = 'green')),
            decreasing = dict(line = dict(color = 'red'))
        )
        '''
        trace2 = gp.Ohlc(
            x = TWTR.index[:],
            open = TWTR['Open'],
            high = TWTR['High'],
            low = TWTR['Low'],
            close = TWTR['Close'],
            name = 'TWTR',
            increasing = dict(line = dict(color='blue')),
            decreasing = dict(line = dict(color='red'))
        )
        trace3 = gp.Ohlc(
            x = AAPL.index[:],
            open = AAPL['Open'],
            high = AAPL['High'],
            low = AAPL['Low'],
            close = AAPL['Close'],
            name = 'AAPL',
            increasing = dict(line = dict(color='yellow')),
            decreasing = dict(line = dict(color='red'))
        )
        '''
        data = [trace1]
        layout =  {
            'title' : self.stockSym + " Analysis",
            'yaxis' : { 'title' : 'Price/Stock'}
        }
        fig = dict(data = data, layout = layout)
        plot_div = py.plot(fig, output_type = 'div')
        return plot_div