from django.core.management.base import BaseCommand
import requests


# this is how you fetch the ioc feeds
def fetch_darklist():
    print("Fetching from darklist...")
    try:
        response = requests.get("https://darklist.de/raw.php")
        response.raise_for_status()
        print(response.text)
    except Exception as e:
        pass

def fetch_blocklist():
    print("Fetching from blocklist...")

def fetch_abuseIPDB():
    print("Fetching from abuse IP DB...")

def fetch_botvrij():
    print("Fetching from botvrij...")




class Command(BaseCommand):
    def handle(self, *args, **options):
        fetch_darklist()
