from django.db import models


class Grupo(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=100) # Matematicas de primer año
	password = models.CharField(max_length=256, null =True)
	# curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
	# usuarios = models.ManyToManyField(User)
