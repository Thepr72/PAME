from datetime import datetime, timedelta
import imp
import json
import numbers
from random import random
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_list_or_404
from authentication.views import User

from lib.extras import generate_token
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib import admin
from django.urls import path


def inicio(request):
    if(request.user.is_authenticated):
        return render(request, 'web/cursos.html', {})

    return render(request, 'web/index.html', {})


def register_request(request):
    if request.method == "POST":
        print(request.POST)
        form = RegisterForm(request.POST)
        print(form)
        if form.is_valid():
            print("Form valid")
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            response = redirect("/numero")
            print(response)
            try:
                token = generate_token(request, user.username)
                response.set_cookie("type", user.type, expires=(
                    datetime.today()+timedelta(days=5)))
                response.set_cookie("token", token, expires=(
                    datetime.today()+timedelta(days=5)))
                return response
            except Exception as e:
                print(e)
                return redirect("/")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
        return JsonResponse(data=form.cleaned_data, status=500, safe=False)
    form = RegisterForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})


def login_request(request):
    response = redirect("/")
    token = generate_token(request, request.user.username)
    response.set_cookie("type", request.user.type, expires=(
        datetime.today()+timedelta(days=5)))

    response.set_cookie("token", token, expires=(
        datetime.today()+timedelta(days=5)))
    return response


def actividades(request):
    return render(request, 'web/actividades.html', {})


def ejercicios(request):
    return render(request, 'web/ejercicios.html', {})


def success(request):
    return render(request, "registration/success.html")


def cursos(request):
    return render(request, 'web/cursos.html', {})


def curso(request):
    return render(request, 'web/curso.html', {})


def cursosAlumno(request):
    return render(request, 'web/cursosAlumno.html', {})


def cursoAlumno(request):
    return render(request, 'web/cursoAlumno.html', {})


def tareaAlumno(request):
    return render(request, 'web/tareaAlumno.html', {})


def numero(request):
    return render(request, 'web/numero.html', {})


def codigo(request):
    response = {"codigo": request.user.Num}
    return JsonResponse(response)
