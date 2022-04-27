import imp
from django.shortcuts import render, redirect, get_list_or_404
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


 

def inicio(request):
    return render(request, 'web/inicio.html', {})


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("inicio.html")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="registration/register.html", context={"register_form":form})

def actividades(request):
	return render(request, 'web/actividades.html', {})

def ejercicios(request):
	return render(request, 'web/ejercicios.html',{})