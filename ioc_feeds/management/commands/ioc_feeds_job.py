from random import randrange
from typing import List
from django.conf import settings
from django.core.management.base import BaseCommand
import requests
from ioc_feeds.producer import KafkaProducerWrapper
from ioc_feeds.models import Stats

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
            "type": "ip",
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
            "type": "ip",
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
            "type": "ip",
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
                    "type": "email",
                    "source": "Botvrij"
                },
                values
            )
        )
        return emails

    except Exception as e:
        print(f"Error: {e}")
        return []


def fetch_urlhaus():
    print("Fetching from URL...")
    try:
        response = requests.get("https://urlhaus.abuse.ch/downloads/text/")
        response.raise_for_status()
        values = response.text.strip().split("\r")[9:]
        urls = list(
            map(lambda url: {
                    "ioc": url.strip(),
                    "type": "url",
                    "source": "URLhaus" 
                },
                values
            )
        )
        return urls
    except Exception as e:
        print(f"Error: {e}")
        return []

def fetch_malware_bazaar():
    print("Fetching from malwareBazaar")

    headers = { 'API-KEY': 'bcdbf6dfe3906f88d361dc88780b78f0' }
    data = {
        'query': 'get_recent',
        'selector': "100",
    }

    try:
        response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=15, headers=headers)
        response.raise_for_status()
        values = response.json()
        samples = values['data']
        hashes = []
        for sample in samples:
            sha256_hash = {
                "ioc": sample['sha256_hash'],
                "type": "sha256",
                "source": "MalwareBazaar"
            }
            sha1_hash = {
                "ioc": sample['sha1_hash'],
                "type": "sha1",
                "source": "MalwareBazaar"
            }
            md5_hash = {
                "ioc": sample['md5_hash'],
                "type": "md5",
                "source": "MalwareBazaar"
            }
            hashes.append(sha256_hash)
            hashes.append(sha1_hash)
            hashes.append(md5_hash)
        return hashes
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
    # whenever the aggregator runs set the new_iocs_count from the stat to 0!
    stats, created = Stats.objects.get_or_create(pk=1)
    stats.new_iocs_count = 0
    stats.save()

    

    ioc_feed_response = []

    botvrij_iocs = fetch_botvrij()
    darklist_iocs = fetch_darklist()
    urlhaus_iocs = fetch_urlhaus()
    malware_bazaar_iocs = fetch_malware_bazaar()
    if len(botvrij_iocs) > 0:
        ioc_feed_response.extend(botvrij_iocs)
    if len(darklist_iocs) > 0:
        ioc_feed_response.extend(darklist_iocs)
    if len(urlhaus_iocs) > 0:
        ioc_feed_response.extend(urlhaus_iocs)
    if len(malware_bazaar_iocs) > 0:
        ioc_feed_response.extend(malware_bazaar_iocs)
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
