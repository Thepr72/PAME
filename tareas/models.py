from django.db import models
from authentication.models import User
from django.utils.translation import gettext_lazy as _


class Homework(models.Model):
    title = models.CharField(_('Titulo'),max_length=256)
    description = models.TextField(null=True)
    file = models.FileField(
        upload_to="courses/homewowrk", null=True, blank=True)
    limit = models.DateField(null=True)
    closed = models.BooleanField(default=False)
    response = models.ManyToManyField('Response', related_name="homework")

    class Meta:
        verbose_name = _('Tarea')
        verbose_name_plural = _('Tareas')

    def __str__(self):
        print(type(self.title))
        return self.title
    
    def update(self, data):
        if 'title' in data.keys():
            self.title = data['title']
        if 'description' in data.keys():
            self.description = data['description']
        if 'limit' in data.keys():
            self.limit = data['limit']
        if 'closed' in data.keys():
            self.closed = data['closed']
        self.save()
    

class Response(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    answer = models.TextField(null=True)
    file = models.FileField(upload_to='course/homework/responses', null=True)
    sent = models.BooleanField(default=False)
    grade = models.FloatField(null=True)

    class Meta:
        verbose_name = _('Respuesta')
        verbose_name_plural = _('Respuestas')