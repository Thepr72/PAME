from django.contrib import admin
from .models import Course, Post

admin.site.register([Course, Post])