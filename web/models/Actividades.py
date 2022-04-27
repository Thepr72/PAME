from nntplib import GroupInfo
from django.db import models

class Actividad(models.Model):

    Id = models.AutoField(primary_key=True)
    grupo = models.IntegerField()
    titulo = models.CharField(max_length=256)
    contenf = models.TextField()