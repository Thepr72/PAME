from django.db import models

class Grupo(models.Model):
  
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=256, null =True)