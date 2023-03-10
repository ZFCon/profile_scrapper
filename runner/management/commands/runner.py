from django.core.management.base import BaseCommand
from runner.models import Configuration
import time
from ._scraper import PeopleFreeSearchCrawler
from pyvirtualdisplay import Display

SLEEP_TIME = 1

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    display = Display(visible=0, size=(800, 600))

    def handle(self, *args, **options):
        configuration = Configuration.get_solo()
        while True:
            configuration.refresh_from_db()

            if configuration.should_run:
                scraper = PeopleFreeSearchCrawler()

                self.display.start()
                scraper.start()
                self.display.stop()
                configuration.should_run = False
                configuration.save()

            time.sleep(SLEEP_TIME)