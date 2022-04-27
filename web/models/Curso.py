from django.db import models

class Curso(models.Model):
  
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100) # Matematicas de primer año
    descripcion = models.CharField(max_length=200)