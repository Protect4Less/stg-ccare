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


# @login_required(login_url='/login')
# def list(request):
# 	template_name = 'partners/list.html'
# 	partners_data = PartnersDAO.get_partners()
# 	context = {"partners_data":partners_data}
# 	return render(request, template_name, context)

@login_required(login_url='/login')
def pending_payment(request):
	template_name = 'claim/pending-payment.html'
	claim_data = ClaimDAO.get_claim_pending_payment(condition={'cpp_payment_mode':'offline'})
	print('claim_data:: ',claim_data)
	context = {"claim_data":claim_data}
	return render(request, template_name, context)

@login_required(login_url='/login')
def received_payment(request):
	response = {}
	error = None
	response_data = {}
	if request.method != 'POST' and not request.is_ajax:
		error = 'Invalid Action'

	if error is None and request.POST and request.is_ajax:
		# print(request.POST)
		cpp_id = request.POST.get('cpp_id',None)
		# partners_document_sent_by = request.user.id
		error = 'Invalid Partner Id' if cpp_id is None else None

	if error is None:
		ClaimDAO.update_claim_pending_payment(column={"cpp_received_sc":"paid"}, condition = {"cpp_id":cpp_id})
		response_data = {"record_updated":True}

	status = True if error is None else False
	response_data = error if error is not None else response_data

	response = {
		"status": ("OK" if status else "NOK"),
		"code": ("200" if status else "201"),
		"message": error,
		"messageDesc": "",
		"responseData":response_data
	}

	return JsonResponse(response)