from django.db import models


class DataSet(models.Model):
    channel = models.CharField(max_length=64)
    country = models.CharField(max_length=4, default='')
    os = models.CharField(max_length=10)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    installs = models.IntegerField()
    spend = models.FloatField()
    revenue = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.channel
