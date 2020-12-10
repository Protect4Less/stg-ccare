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
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string

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
	partner_code = request.POST.get('partner_code',None)

	if excel_file is not None and partner_code is not None:

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
			print("===================================================")
			for cell in row:
				cell_coordinate = coordinate_from_string(cell.coordinate)
				row_number = cell_coordinate[1]

				if cell.value == "invoice_no" :
					invoice_no_coordinate = coordinate_from_string(cell.coordinate)
					invoice_no_col = invoice_no_coordinate[0]

				if cell.value == "sku" :
					sku_coordinate = coordinate_from_string(cell.coordinate)
					sku_col = sku_coordinate[0]

				if cell.value == "device" :
					device_coordinate = coordinate_from_string(cell.coordinate)
					device_col = device_coordinate[0]

				if cell.value == "model" :
					model_coordinate = coordinate_from_string(cell.coordinate)
					model_col = model_coordinate[0]

				if cell.value == "purchase_month" :
					purchase_month_coordinate = coordinate_from_string(cell.coordinate)
					purchase_month_col = purchase_month_coordinate[0]

				if cell.value == "first_name" :
					first_name_coordinate = coordinate_from_string(cell.coordinate)
					first_name_col = first_name_coordinate[0]

				if cell.value == "last_name" :
					last_name_coordinate = coordinate_from_string(cell.coordinate)
					last_name_col = last_name_coordinate[0]

				if cell.value == "email" :
					email_coordinate = coordinate_from_string(cell.coordinate)
					email_col = email_coordinate[0]

				if cell.value == "mobile_number" :
					mobile_number_coordinate = coordinate_from_string(cell.coordinate)
					mobile_number_col = mobile_number_coordinate[0]

				if cell.value == "imei_serial_no" :
					imei_serial_no_coordinate = coordinate_from_string(cell.coordinate)
					imei_serial_no_col = imei_serial_no_coordinate[0]

				if cell.value == "term_type" :
					term_type_coordinate = coordinate_from_string(cell.coordinate)
					term_type_col = term_type_coordinate[0]

				if cell.value == "device_value" :
					invoice_value_coordinate = coordinate_from_string(cell.coordinate)
					invoice_value_col = invoice_value_coordinate[0]

				if cell.value == "device_currency" :
					device_currency_coordinate = coordinate_from_string(cell.coordinate)
					device_currency_col = device_currency_coordinate[0]

				if cell.value == "brand" :
					brand_coordinate = coordinate_from_string(cell.coordinate)
					brand_col = brand_coordinate[0]


			device_currency_cell = "{}{}".format(device_currency_col, row_number )
			device_currency_value =  str(worksheet[device_currency_cell].value)

			invoice_value_cell = "{}{}".format(invoice_value_col, row_number )
			invoice_value_value =  str(worksheet[invoice_value_cell].value)

			term_type_cell = "{}{}".format(term_type_col, row_number )
			term_type_value =  str(worksheet[term_type_cell].value)

			imei_serial_no_cell = "{}{}".format(imei_serial_no_col, row_number )
			imei_serial_no_value =  str(worksheet[imei_serial_no_cell].value)

			mobile_number_cell = "{}{}".format(mobile_number_col, row_number )
			mobile_number_value =  str(worksheet[mobile_number_cell].value)

			email_cell = "{}{}".format(email_col, row_number )
			email_value =  str(worksheet[email_cell].value)

			last_name_cell = "{}{}".format(last_name_col, row_number )
			last_name_value =  str(worksheet[last_name_cell].value)

			first_name_cell = "{}{}".format(first_name_col, row_number )
			first_name_value =  str(worksheet[first_name_cell].value)

			purchase_month_cell = "{}{}".format(purchase_month_col, row_number )
			purchase_month_value =  str(worksheet[purchase_month_cell].value)

			model_cell = "{}{}".format(model_col, row_number )
			model_value =  str(worksheet[model_cell].value)

			device_cell = "{}{}".format(device_col, row_number )
			device_value =  str(worksheet[device_cell].value)

			invoice_no_cell = "{}{}".format(invoice_no_col, row_number )
			invoice_no_value =  str(worksheet[invoice_no_cell].value)

			sku_cell = "{}{}".format(sku_col, row_number )
			sku_value =  str(worksheet[sku_cell].value)

			brand_cell = "{}{}".format(brand_col, row_number )
			brand_value =  str(worksheet[brand_cell].value)

			#row_data.append(str(cell.value))
			#excel_data.append(row_data)
			# Query = "INSERT INTO `partners_offline_policy_data` ( `popd_invoice_no`, `popd_sku`, `popd_device`, `popd_brand`, `popd_model`, `popd_purchase_month`, `popd_first_name`, `popd_last_name`, `popd_email`, `popd_mobile_number`, `popd_imei_serial_no`, `popd_term_type`, `popd_device_value`, `popd_device_currency`, `popd_addedon`, `popd_updatedon`) VALUES ("
			if row_number != 1:
				PartnersDAO.insert_partners_offline_policy_data({
					'popd_partner_code':partner_code,
					'popd_invoice_no':invoice_no_value,
					'popd_invoice_value':invoice_value_value,
					'popd_sku':sku_value,
					'popd_device':device_value,
					'popd_brand':brand_value,
					'popd_model':model_value,
					'popd_purchase_month':purchase_month_value,
					'popd_first_name':first_name_value,
					'popd_last_name':last_name_value,
					'popd_email':email_value,
					'popd_mobile_number':mobile_number_value,
					'popd_imei_serial_no':imei_serial_no_value,
					'popd_term_type':term_type_value,
					'popd_device_currency':device_currency_value})

				
				# Query = "INSERT INTO `partners_offline_policy_data` ( `popd_invoice_no`, `popd_sku`, `popd_device`, `popd_brand`, `popd_model`, `popd_purchase_month`, `popd_first_name`, `popd_last_name`, `popd_email`, `popd_mobile_number`, `popd_imei_serial_no`, `popd_term_type`, `popd_device_value`, `popd_device_currency`, `popd_addedon`, `popd_updatedon`) VALUES ('" + invoice_no_value +"','"+ sku_value +"','"+ device_value +"','"+ brand_value +"','"+ model_value +"','"+ purchase_month_value +"','"+ first_name_value +"','"+ last_name_value +"','"+ email_value +"','"+ mobile_number_value +"','"+ imei_serial_no_value +"','"+ term_type_value +"','"+ invoice_value_value +"','"  + device_currency_value +"'," + "current_timestamp(), current_timestamp())"

				# print('\n\n', Query , '\n\n')
				# cursor = connection.cursor()
				# cursor.execute(Query)

		messages.success(request, 'File Uploaded successfuly. Data will be processed')
	template_name = 'partners/upload_create_policy.html'
	partners_obj = PartnersDAO.get_partners(condition={'partners_status':'active'})
	#print('partners_obj:: ',partners_obj)
	context = {"partners_obj":partners_obj}
	return render(request, template_name, context)
