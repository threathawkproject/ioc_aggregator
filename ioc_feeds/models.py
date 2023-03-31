from django.db import models


# Enum for our Indicator types
class IndicatorType(models.TextChoices):
    IP = "ip"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    Domain = "domain"
    Email = "email"
    URL = "url"
    File = "file"
# Data model for our IOC

class Ioc(models.Model):
    ioc = models.TextField(primary_key=True)
    type = models.TextField(choices=IndicatorType.choices)
    sources = models.JSONField()
    frequency = models.IntegerField(default=1)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    location = models.JSONField(null=True)

    # string representation of the model
    def __str__(self):
        return f"Ioc: {self.ioc} | Type: {self.type} | Source: {self.sources} | Frequency: {self.frequency} | Created At: {self.created_timestamp} | Updated At: {self.updated_timestamp} | Location: {self.location}"  
    

class Stats(models.Model):
    new_iocs_count = models.PositiveIntegerField(default=0)
    frequent_iocs_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Stats #{self.pk}: new_iocs_count={self.new_iocs_count}, frequent_iocs_count={self.frequent_iocs_count}'