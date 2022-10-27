from django.core.management.base import BaseCommand
from ioc_feeds.consumer import KafkaConsumerWrapper
from ioc_feeds.models import Ioc

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Waiting to consume!")
        # using the wrapper
        consumer = KafkaConsumerWrapper.instance()
        # counter = 0
        for ioc in consumer:
            resp = ioc.value
            ioc = Ioc.objects.create(
                ioc=resp["ioc"],
                type=resp["type"],
                source=resp["source"]
            )
            print(resp)