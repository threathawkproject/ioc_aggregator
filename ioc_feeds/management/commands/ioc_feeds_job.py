from random import randrange
from typing import List
from django.conf import settings
from django.core.management.base import BaseCommand
import requests
from ioc_feeds.producer import KafkaProducerWrapper
import time

# Third party libraries
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


# Each function fetches indicators from a different source
def fetch_darklist():
    print("Fetching indicators from Darklist...")

    try:
        response = requests.get("https://darklist.de/raw.php")
        response.raise_for_status()

        ip_addresses = response.text.strip().split()[11:]
        iocs = list(map(lambda ip: {
            "ioc": ip,
            "type": "IP",
            "source": "Darklist"
        },
            ip_addresses
        ))
        return iocs

    except Exception as e:
        print(f"Error occured: {e}")
        return []


def fetch_blocklist():
    print("Fetching indicators from Blocklist...")

    try:
        response = requests.get("https://lists.blocklist.de/lists/all.txt")
        response.raise_for_status()

        ip_addresses = response.text.strip().split("\n")
        iocs = list(map(lambda ip: {
            "ioc": ip,
            "type": "IP",
            "source": "Blocklist"
        },
            ip_addresses
        ))
        return iocs

    except Exception as e:
        print(f"Error")
        return []


def fetch_abuseIPDB():
    print("Fetching indicators from AbuseIPDB...")

    try:
        headers = {"Key": "aa08332f175a5c5b3ef2c4606197aad7d7a83df1a68b119c302ba6cd9156f7f097f8757b738bb840",
                   "Accept": "application/json"}
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/blacklist", headers=headers)
        response.raise_for_status()

        data = response.json()
        iocs = list(map(lambda element: {
            "ioc": element["ipAddress"],
            "type": "IP",
            "source": "AbuseIPDB",
            "location": element["countryCode"]
        },
            data["data"]
        ))
        return iocs

    except Exception as e:
        print(f"Error: {e}")
        return []


def fetch_botvrij():
    print("Fetching from Botvrij...")

    try:
        response = requests.get(
            "https://www.botvrij.eu/data/ioclist.email-src")
        response.raise_for_status()

        values = response.text.strip().split("\n")[6:]
        emails = list(
            map(lambda sentence: {
                "ioc": sentence.strip().split(" ")[0],
                "type": "Email",
                "source": "Botvrij"
            },
                values
            )
        )
        return emails

    except Exception as e:
        print(f"Error: {e}")
        return []


def publish(iocs):
    try:
        producer = KafkaProducerWrapper.instance()
        for ioc in iocs:
            producer.send("ioc_feed", ioc)
            # time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")


class run_aggregator():
    ioc_feed_response = []

    botvrij_iocs = fetch_botvrij()
    if len(botvrij_iocs) > 0:
        ioc_feed_response.extend(botvrij_iocs)

    darklist_iocs = fetch_darklist()
    if len(darklist_iocs) > 0:
        ioc_feed_response.extend(darklist_iocs)

    publish(ioc_feed_response)


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
