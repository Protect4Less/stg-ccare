from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(request):
	return redirect('dashboard:dashboard')