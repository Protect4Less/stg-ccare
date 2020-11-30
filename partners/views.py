from django.shortcuts import render, redirect
from django.http import  HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from backend.dao.PartnersDAO import PartnersDAO
# from backend.dao.CampaignDAO import CampaignDAO
# from backend.dao.MasterDAO import MasterDAO
# from backend.lib.CommonLib import CommonLib
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.utils.encoding import smart_str
import datetime
import json
from backend.dao.ClaimDAO import ClaimDAO
# import os
from django.conf import settings
from django.http import HttpResponse, Http404
import xlrd

# @login_required(login_url='/login')
# def list(request):
# 	template_name = 'partners/list.html'
# 	partners_data = PartnersDAO.get_partners()
# 	context = {"partners_data":partners_data}
# 	return render(request, template_name, context)

# @login_required(login_url='/login')
# def upload_create_policy(request):
# 	template_name = 'claim/pending-payment.html'
# 	claim_data = ClaimDAO.get_claim_pending_payment(condition={'cpp_payment_mode':'offline'})
# 	print('claim_data:: ',claim_data)
# 	context = {"claim_data":claim_data}
# 	return render(request, template_name, context)

@login_required(login_url='/login')
def upload_create_policy(request):
	response = {}
	error = None


 
	loc = ("/home/tmt/Documents/Prem/p4l_item_invoiced.xlsx")
	 
	wb = xlrd.open_workbook(loc)
	sheet = wb.sheet_by_index(0)
	
	sheet.cell_value(0, 0)
 
	print(sheet.row_values(1))
	 
	# Extracting number of columns
	print(sheet.ncols)
	template_name = 'partners/upload_create_policy.html'
	partners_obj = PartnersDAO.get_partners(condition={'partners_status':'active'})
	print('partners_obj:: ',partners_obj)
	context = {"partners_obj":partners_obj}
	return render(request, template_name, context)