from imp import source_from_cache
from django.db import models

# Create your models here.
class Ioc(models.Model):
    ioc = models.TextField()
    type = models.TextField()
    source = models.TextField()