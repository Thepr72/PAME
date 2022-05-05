from django.contrib import admin
from .models import Homework, Response

admin.site.register([Homework, Response])