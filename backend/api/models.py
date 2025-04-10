from django.db import models

class Project(models.Model):
    ts = models.DateTimeField()
    lat = models.FloatField()
    lon = models.FloatField()
    temperature = models.FloatField()
    pressure = models.FloatField()
    humidity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'project'
