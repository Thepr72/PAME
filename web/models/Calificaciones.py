from pickle import TRUE
from django.db import models

class Calificaciones(models.Model):
    
    id = models.AutoField(primary_key=True)
    alumno = models.IntegerField()
    actividad = models.IntegerField()
    calificacion = models.IntegerField()