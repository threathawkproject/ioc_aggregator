from django.core.management.base import BaseCommand
from ioc_feeds.consumer import KafkaConsumerWrapper
import ioc_feeds.utils
 


# This is the job that runs consumer which ingests the IOC and checks for the following
# 1. Is Added if so update it!
# 2. Is not add it in our DB
class Command(BaseCommand):
    def handle(self, *args, **options):
        print(f"ready to consume!!")
        # using the Kafka singleton instance
        consumer = KafkaConsumerWrapper.instance()
        for ioc in consumer:
            # checking if the ioc exists in our db
            is_added = ioc_feeds.utils.is_added(ioc.value)
            if is_added:
                # update it!
                ioc_feeds.utils.update(ioc.value)
            else:
                # add it!
                ioc_feeds.utils.add(ioc.value)
        
