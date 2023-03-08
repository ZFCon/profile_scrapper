import os
import time
import pandas as pd
from scrapy import Selector

from urllib import  parse 
from selenium import webdriver
import undetected_chromedriver as uc




class PeopleFreeSearchCrawler():
	input_file = './searchpeoplefree.csv'

	def __init__(self):
		self.df = pd.read_csv(self.input_file)
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--blink-settings=imagesEnabled=false')
		self.driver = uc.Chrome(version_main=109, options=chrome_options)
		self.driver.maximize_window()
	
	def start(self):
		try:
			with open('status.csv', 'r') as f:
				index = int(f.read())
		except Exception as e:
			print(e)
			index = 0
		for index, row in self.df.iloc[index:,:].iterrows():
			url = row['Link']
			print('Scraping... {}/{} === {}'.format(index, self.df.shape[0], url))
			while True:
				try:
					self.driver.get(url)
					break
				except:
					chrome_options = webdriver.ChromeOptions()
					chrome_options.add_argument('--blink-settings=imagesEnabled=false')
					self.driver = uc.Chrome(version_main=109, options=chrome_options)
					self.driver.maximize_window()
					print('Trying again!')

			selector = Selector(text=self.driver.page_source)
			name = selector.css('ol.inline > li:nth-child(1) article span.d-block::text').get()
			if not name:
				name = selector.css('ol.inline > li:nth-child(1) article h2::text').get()
			if not name:
				continue
				
			phones = selector.xpath('//ol/li[1]//article[1]//ul//a[contains(@href, "phone-lookup")]//text()').extract()
			for n, phone in enumerate(phones):
				self.df.loc[index, 'Phone {}'.format(n+1)] = phone

			self.df.loc[index, 'Name'] = name.strip()
			self.df.to_csv('./searchpeoplefree.csv', index=False)

			with open('status.csv', 'w') as f:
				f.write(str(index))
		
		os.system('rm status.csv')

if __name__ == '__main__':
	scraper = PeopleFreeSearchCrawler()
	scraper.start()
