from django.core.management.base import BaseCommand
from runner.models import Configuration
import time
from ._scraper import PeopleFreeSearchCrawler

SLEEP_TIME = 1

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        configuration = Configuration.get_solo()
        while True:
            configuration.refresh_from_db()

            if configuration.should_run:
                scraper = PeopleFreeSearchCrawler()
                scraper.start()
                configuration.should_run = False
                configuration.save()

            time.sleep(SLEEP_TIME)