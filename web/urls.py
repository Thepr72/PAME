import email
from django.urls import path
from . import views
from django.urls import re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.inicio, name='inicio'),
    re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    #    re_path(r'^admin/', admin.site.urls),
    path("register", views.register_request, name="register"),
    path("actividades", views.actividades, name="actividades"),
    path("ejercicios", views.ejercicios, name="ejercicios"),
    path("success", views.success, name="success"),
    path("cursos", views.cursos, name="cursos"),
    path("curso", views.curso, name="curso"),
    path("cursosAlumno", views.cursosAlumno, name="cursosAlumno"),
    path("cursoAlumno", views.cursoAlumno, name="cursoAlumno"),
    path("tareaAlumno", views.tareaAlumno, name="tareaAlumno"),
]

urlpatterns += staticfiles_urlpatterns()
