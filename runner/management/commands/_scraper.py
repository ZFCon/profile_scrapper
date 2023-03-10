import pandas as pd
from scrapy import Selector
from pyvirtualdisplay import Display

from selenium import webdriver
import undetected_chromedriver as uc
from runner.models import Configuration




class PeopleFreeSearchCrawler():
    configuration = Configuration.get_solo()

    def __init__(self, input_file='./searchpeoplefree.csv'):
        self.input_file = input_file
        self.df = pd.read_csv(self.input_file)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = uc.Chrome(version_main=109, options=chrome_options)
        self.driver.maximize_window()
        self.configuration.refresh_from_db()
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
    
    def start(self):
        index = self.configuration.skip_traced
        total_count = self.df.shape[0]

        self.configuration.total_count = total_count
        self.configuration.save()

        for index, row in self.df.iloc[index:,:].iterrows():
            self.configuration.refresh_from_db()
            # save progress.
            self.configuration.skip_traced = index
            self.configuration.save()
            
            if not self.configuration.should_run:
                self.driver.close()
                self.display.stop()
                break

            url = row['Link']
            print('Scraping... {}/{} === {}'.format(index, total_count, url))
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
            self.df.to_csv(self.input_file, index=False)
            
            if index + 1 == total_count:
                self.configuration.skip_traced = 0
                self.configuration.should_run = False
                self.configuration.save()
                self.display.stop()

if __name__ == '__main__':
    scraper = PeopleFreeSearchCrawler()
    scraper.start()