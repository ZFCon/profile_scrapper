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

            try:
                if configuration.should_run:
                    scraper = PeopleFreeSearchCrawler(configuration.runner_file.path)

                    scraper.start()

                    configuration.should_run = False
                    configuration.save()
            except:
                pass

            time.sleep(SLEEP_TIME)