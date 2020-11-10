from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# from backend.dao.DashboardSummaryDAO import DashboardSummaryDAO

# Create your views here.


def logout_view(request):
	logout(request)
	return redirect("/")


@login_required(login_url='/login')
def dashboard(request):
	print('hiee')
	template_name = 'dashboard/dashboard.html'
	context = {}
	return render(request,template_name,context)