from django.core.management.base import BaseCommand
import requests
from IPy import IP


# this is how you fetch the ioc feeds
def fetch_darklist():
    print("Fetching from darklist...")
    try:
        response = requests.get("https://darklist.de/raw.php")
        response.raise_for_status()
        ip_addresses = response.text.strip().split()[11:]
        iocs = []
        for ip in ip_addresses:
            ioc = {
                "ioc": ip,
                "source": "darklist"
            }
            iocs.append(ioc)
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




class Command(BaseCommand):
    def handle(self, *args, **options):
        ioc_feed_respone = []
        darklist_iocs = fetch_darklist()
        if len(darklist_iocs) > 0:
            ioc_feed_respone.extend(darklist_iocs)
        print(ioc_feed_respone)
        print("ioc_feed_respone")
