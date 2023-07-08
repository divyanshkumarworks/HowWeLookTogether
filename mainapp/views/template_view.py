from django.shortcuts import render

def home(request):
	return render(request, "mainapp/home.html")

def landing(request):
	return render(request, "mainapp/landing.html")