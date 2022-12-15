from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=150, default = None)

    def __str__(self):
        return self.name

class MountainRange(models.Model):
    name = models.CharField(max_length=150, default = None)

    def __str__(self):
        return self.name


class AboutSummit(models.Model):
    title = models.CharField(max_length=200, default = None)
    high = models.PositiveIntegerField(default = 0)
    description = models.TextField(default = None)
    long_pos = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    lat_pos = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    mountainrange = models.ForeignKey(MountainRange, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
