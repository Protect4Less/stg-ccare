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
import openpyxl
from django.db import connection

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
	excel_file = request.FILES.get('item_data_excel', None)


	if excel_file is not None:

		excel_file = request.FILES['item_data_excel']
		wb = openpyxl.load_workbook(excel_file)
		worksheet = wb["Sheet1"]
		print(worksheet)

		excel_data = list()
		cnt = 0
		cntin = 0

		excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
		for row in worksheet.iter_rows():
			row_data = list()
			Query = "INSERT INTO `partners_offline_policy_data` ( `popd_invoice_no`, `popd_sku`, `popd_device`, `popd_brand`, `popd_model`, `popd_purchase_month`, `popd_first_name`, `popd_last_name`, `popd_email`, `popd_mobile_number`, `popd_imei_serial_no`, `popd_term_type`, `popd_device_value`, `popd_device_currency`, `popd_addedon`, `popd_updatedon`) VALUES ("
			print("===================================================")
			for cell in row:
				Query = Query +"'"+ str(cell.value) + "', "

				"'', '', '', '', '', NULL, '', '', '', '', '', '', '', '', '0', '0', '0', '', '', '', current_timestamp(), current_timestamp());"
				#row_data.append(str(cell.value))
				#excel_data.append(row_data)
			Query = Query + "current_timestamp(), current_timestamp())"
			print('\n\n', Query , '\n\n')
			#print('\n\n\n', excel_data , '\n\n\n')
			cursor = connection.cursor()
			cursor.execute(Query)


	# loc = ("/home/tmt/Documents/Prem/p4l_item_invoiced.xlsx")
	#
	# wb = xlrd.open_workbook(loc)
	# sheet = wb.sheet_by_index(0)
	#
	# sheet.cell_value(0, 0)
	#
	# print(sheet.row_values(1))
	#
	# # Extracting number of columns
	# print(sheet.ncols)
	template_name = 'partners/upload_create_policy.html'
	partners_obj = PartnersDAO.get_partners(condition={'partners_status':'active'})
	print('partners_obj:: ',partners_obj)
	context = {"partners_obj":partners_obj}
	return render(request, template_name, context)
