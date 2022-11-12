from random import randrange
from typing import List
from django.conf import settings
from django.core.management.base import BaseCommand
import requests
from ioc_feeds.producer import KafkaProducerWrapper
import time


# Third party
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
# this is how you fetch the ioc feeds
def fetch_darklist():
    print("Fetching from darklist...")
    try:
        response = requests.get("https://darklist.de/raw.php")
        response.raise_for_status()
        ip_addresses = response.text.strip().split()[11:]
        iocs = list(map(lambda ip : {
                "ioc": ip,
                "type": "IP",
                "source": "darklist"
            },
            ip_addresses
        ))
        return iocs
    except Exception as e:
        print(f"Error occured: {e}")
        return []

def fetch_blocklist():
    print("Fetching from blocklist...")

def fetch_abuseIPDB():
    print("Fetching from abuse IP DB...")

def fetch_botvrij():
    print("Fetching from botvrij...")
    try:
        response = requests.get("https://www.botvrij.eu/data/ioclist.email-src")
        response.raise_for_status()
        values = response.text.strip().split("\n")[6:]
        emails = list(
            map(lambda sentence: {
                    "ioc": sentence.strip().split(" ")[0],
                    "type": "email",
                    "source": "botvrij"
                }, 
                values
            )
        )
        return emails
    except Exception as e:
        return []
def publish(iocs):
    try:
        producer = KafkaProducerWrapper.instance()
        for ioc in iocs:
            producer.send("ioc_feed", ioc)
            # time.sleep(1)
    except Exception as e:
        print(f"Error occured: {e}")

class run_aggregator():
        ioc_feed_respone = []
        botvrij_iocs = fetch_botvrij()
        darklist_iocs = fetch_darklist()
        if len(botvrij_iocs) > 0:
            ioc_feed_respone.extend(botvrij_iocs)
        if len(darklist_iocs) > 0:
            ioc_feed_respone.extend(darklist_iocs)
        # print(ioc_feed_respone)
        publish(ioc_feed_respone)

class Command(BaseCommand):
    def handle(self, *args, **options):
        run_aggregator()
        # scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        # scheduler.add_jobstore(DjangoJobStore(), "default")

        # scheduler.add_job(
        #     run_aggregator,
        #     trigger="interval",
        #     minutes=5,
        #     id="Aggregator",
        #     max_instances=1,
        #     replace_existing=True,
        # )

        # try:
        #     print("Starting scheduler...")
        #     scheduler.start()
        # except KeyboardInterrupt:
        #     print("Stopping scheduler...")
        #     scheduler.shutdown()
        #     print("Scheduler shut down successfully!")


        # ioc_feed_respone = []
        # botvrij_iocs = fetch_botvrij()
        # darklist_iocs = fetch_darklist()
        # if len(botvrij_iocs) > 0:
        #     ioc_feed_respone.extend(botvrij_iocs)
        # if len(darklist_iocs) > 0:
        #     ioc_feed_respone.extend(darklist_iocs)
        
        # print(ioc_feed_respone)

        # print(ioc_feed_respone)
        # publish(ioc_feed_respone)
