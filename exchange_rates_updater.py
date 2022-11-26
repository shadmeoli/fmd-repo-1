"""
	Instred of hard-coding the exchange rates;
	this script will help automate the process.

	This "webhook" will help update the exchange rate
	every time the user runs the app

	I am using:
		- requests
		- beautiful soup


	I am using this website to get the rates 
	<https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=KES>
"""

from datetime import datetime

import requests
from bs4 import BeautifulSoup


# main entry class
class CurrentRate:

	def __init__(self):

		self.current_date = datetime.utcnow()
		self.URL = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=KES'


	# a beautiful soup crawler to the website
	def crawler(self): # parse in to_<currency> -> to convert from USD to Kes and opposite

		# get response of the url
		result = requests.get(self.URL)
		# soup crawler
		soup = BeautifulSoup(result.text, "html.parser")
		# tag locator 
		exchnge_rates = soup.find_all('p', attrs={'class' : 'result__BigRate-sc-1bsijpp-1 iGrAod'})
		# current market rates
		curr_exchange_rates = exchnge_rates[0].text
		rate_value = float(curr_exchange_rates[:curr_exchange_rates.rfind('K')-1])

		return round(rate_value, 2)



# manual test
if __name__ == '__main__':
	current_rate = CurrentRate()
	print(current_rate.crawler())