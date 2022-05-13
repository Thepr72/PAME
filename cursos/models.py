from datetime import datetime
from django.db import models
from authentication.models import User
from tareas.models import Homework
from django.utils.translation import gettext_lazy as _

class Post(models.Model):

    title = models.CharField(_('Titulo'), max_length=256, null=True)
    content = models.TextField(null=True)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, null=True)
    timestamp = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('Publicacion')
        verbose_name_plural = _('Publicaciones')


    def update(self, data):
        if 'title' in data:
            self.title = data['title']
        if 'content' in data:
            self.content = data['content']
        if 'file' in data:
            self.file = data['file']

        self.save()


class Course(models.Model):

    class Meta:
        verbose_name = _('Curso')
        verbose_name_plural = _('Cursos')
    
    name = models.CharField(max_length=256)
    password = models.CharField(max_length=256, null=True)
    professor = models.ManyToManyField(
        User, related_name="course_professor", symmetrical=False)
    activate = models.BooleanField(default=True)
    students = models.ManyToManyField(
        User, related_name="student_courses")
    homework = models.ManyToManyField(
        Homework, related_name="course")
    post = models.ManyToManyField(Post, related_name="course")
    description = models.TextField(null=True)
    created = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return self.name


    def uptade(self, data):
        if 'name' in data:
            self.name = data['name']
        if 'password' in data:
            self.password = data['password']
        if 'activate' in data:
            self.activate = data['activate']

        
        self.save()


        
    
    

    