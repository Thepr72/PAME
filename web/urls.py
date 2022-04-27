import email
from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.inicio, name='inicio'),
   url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
   url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
   url(r'^admin/', admin.site.urls),
   path("register", views.register_request, name="register"),
   path("actividades",views.actividades, name="actividades"),
   path("ejercicios", views.ejercicios, name="ejercicios" ),
    
]

urlpatterns += staticfiles_urlpatterns()

