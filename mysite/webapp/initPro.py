import re
import dateutil.parser as parser
import linkGrabber
import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd
from datetime import date, timedelta
import httplib2
from . import stockAnalysis
from . import techStockViz
from . import techStockData
import datetime

def GetRecords(YEAR):
	# DECLARING .CSV OUTPUT FILE
	CSV_FILE = r"OrbitalLaunchesOutput.csv"

	# YOU CAN MODIFY THE YEAR
	#YEAR = "2019"

	# URL TO SERACH
	URL = 'https://en.wikipedia.org/wiki/' + YEAR + '_in_spaceflight#Orbital_launches'

	# GET REQUEST (HTML FORMAT)
	RESPONSE = requests.get(URL, allow_redirects=True)

	CONTENT_OF_PAGE = RESPONSE.content
	FILE1 = open("page.html", "w")
	FILE1.write(str(CONTENT_OF_PAGE))
	FILE2 = open("page.html", "r")
	CONTENT_HTML = FILE2.read()
	FILE1.close()

	SOUP = BeautifulSoup(CONTENT_HTML, features="lxml")
	FILE2.close()

	# print('***************************************************************************************************************************')

	TABLE = SOUP.find('table', {'class': 'wikitable'})
	# print(table)
	ROWS = list()
	COUNTER = 0

	DatesDict = dict()

	START_DATE_OF_YEAR = date(int(YEAR), 1, 1)  # start date
	END_DATE_OF_YEAR = date(int(YEAR), 12, 31)  # end date

	DATE_DAYS = END_DATE_OF_YEAR - START_DATE_OF_YEAR  # as timedelta
	COUNT_DAYS = 0
	for i in range(DATE_DAYS.days + 1):
		DAY = START_DATE_OF_YEAR + timedelta(days=i)
		COUNT_DAYS += 1
		DATE = parser.parse(str(DAY))
		ISO_DATE = DATE.isoformat()
		DatesDict[ISO_DATE] = 0
	print(COUNT_DAYS)

	START_OF_LAUNCH_FLAG = 0
	NewTag = ""

	for ROW in TABLE.findAll("tr"):
		# i = soup.select("span.nowrap")
		# print('__________________________________________________________________________________________________________________________')
		# print(ROW)

		if (str(ROW)[28:42] == 'class="nowrap"' or str(ROW)[29:43] == 'class="nowrap"'):
			START_OF_LAUNCH_FLAG = 1
			# print('__________________________________________________________________________________________________________________________')
			# print(ROW)
			left = 'class="nowrap">'
			right = 0
			# Output: 'string'
			s = str(ROW)
			le = s.index(left) + len(left)
			ri = s.index(left) + 30
			Tag = (str(ROW)[le:ri])
			NewTag = re.sub('<(.*)', '', Tag) + ', ' + YEAR
		# print(NewTag)

		else:
			if START_OF_LAUNCH_FLAG == 1:
				STATUS = str(ROW)[-200:]
				if 'Successful' in STATUS or 'Operational' in STATUS or 'En Route' in STATUS:
					START_OF_LAUNCH_FLAG = 0
					try:
						DATE = parser.parse(NewTag)
						ISO_DATE = DATE.isoformat()
						# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
						print(ISO_DATE)
						if ISO_DATE in DatesDict:
							DatesDict[ISO_DATE] += 1
							COUNTER += 1
					except:
						print("~~~~~~~ KEY ERROR ~~~~~~~")

	# print(DatesDict)

	DataFrame = pd.DataFrame(list(DatesDict.items()), columns=['date', 'value'])
	DataFrame.index = DataFrame.index + 1
	print(DataFrame)
	print(COUNTER)
	#DataFrame.to_csv(CSV_FILE, index=False)
	return DataFrame

def getlink(YEAR):
	frame = GetRecords(YEAR)
	return frame

def getStockAnalysis(stockName):
	startDate = datetime.datetime(2021, 1, 1)
	endDate = datetime.datetime(2021, 12, 10)
	stockAnaObj = stockAnalysis.StockAnalysis(stockName, startDate, endDate)
	stockAnaObj.beginAnalysis2()

	#stockObj = techStockData.TechStockData(s)
	#df = stockObj.getStockData()
	stockVizObj = techStockViz.TechStock(stockName, startDate, endDate)
	plot_div = stockVizObj.getTechStock()
	return stockAnaObj.df, plot_div