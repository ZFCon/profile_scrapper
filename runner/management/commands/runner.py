from django.core.management.base import BaseCommand
from runner.models import Configuration
import time
from ._scraper import PeopleFreeSearchCrawler
import undetected_chromedriver as uc
from selenium import webdriver

SLEEP_TIME = 1

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        configuration = Configuration.get_solo()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        driver = uc.Chrome(version_main=109, options=chrome_options)
        driver.maximize_window()
        import pdb
        pdb.set_trace()

        while True:
            configuration.refresh_from_db()

            try:
                if configuration.should_run:
                    scraper = PeopleFreeSearchCrawler(driver, configuration.runner_file.path)

                    scraper.start()

                    configuration.should_run = False
                    configuration.save()
            except:
                pass

            time.sleep(SLEEP_TIME)