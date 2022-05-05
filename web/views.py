import imp
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_list_or_404
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages

def inicio(request):
	if(request.user.is_authenticated):
		return render(request, 'web/actividades.html', {})
	
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
			messages.success(request, "Registration successful." )
			return HttpResponseRedirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
		print(form.data)
		return JsonResponse(data=form.cleaned_data, status=500, safe=False)
	form = RegisterForm()
	return render(request=request, template_name="registration/register.html", context={"register_form":form})

def actividades(request):
	return render(request, 'web/actividades.html', {})

def ejercicios(request):
	return render(request, 'web/ejercicios.html',{})

def success(request):
	return render(request, "registration/success.html")