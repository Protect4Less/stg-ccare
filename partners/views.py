from django.shortcuts import render, redirect
# from django.http import  HttpResponse
# from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from backend.dao.PartnersDAO import PartnersDAO
# from backend.dao.CampaignDAO import CampaignDAO
# from backend.dao.MasterDAO import MasterDAO
# from backend.lib.CommonLib import CommonLib
from django.contrib import messages
# from django.contrib.auth.hashers import make_password
# from django.http import JsonResponse
# from django.utils.encoding import smart_str
# import datetime
# import json
# from backend.dao.ClaimDAO import ClaimDAO
# import os
# from django.conf import settings
# from django.http import HttpResponse, Http404
# import xlrd
import openpyxl
# from django.db import connection
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
import logging
logger = logging.getLogger(__name__)


@login_required(login_url='/login')
def upload_create_policy(request):
    response = {}
    error = None
    excel_file = request.FILES.get('item_data_excel', None)
    partner_code = request.POST.get('partner_code',None)

    partners_config = [{"id":1025, "name":'1025 - SAFARI HYPER MARKET - SADIQ ALI'},{"id":1026, "name":'1026 - NESTO GROUP - MR. FARHAN MOHAMED'},{"id":'RG', "name":'RG - Redington'},{"id":1030, "name": '1030 - TECH-OFFER (FLORENCE TRD)'},{ "id": 1031, "name":'1031 - THOMSUN PLAY'}, {"id":1014, "name":'1014 - Florance'}, {"id":1035, "name":'1035 - jacky'}]

    if excel_file is not None and partner_code is not None:

        excel_file = request.FILES['item_data_excel']
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        cnt = 0
        cntin = 0

        excel_data = list()
        cell_values = []
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            print("===================================================", row)
            for cell in row:
                cell_coordinate = coordinate_from_string(cell.coordinate)
                row_number = cell_coordinate[1]
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$", cell_coordinate)
                print ("$$$$$$$$$$$$$$$$$$$$$$$$$$", row_number)
                if cell.value in ["",None," "]:
                    continue

                cell.value = cell.value.strip() if isinstance(cell.value,str) else cell.value
                print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", cell.value)
                cell_values.append(cell.value)

                if cell.value in ["invoice_no", "Invoice Number"] :
                    invoice_no_coordinate = coordinate_from_string(cell.coordinate)
                    invoice_no_col = invoice_no_coordinate[0]

                if cell.value in ["sku","SKU ( Article )","Part#","Part"] :
                    sku_coordinate = coordinate_from_string(cell.coordinate)
                    sku_col = sku_coordinate[0]

                if cell.value in ["location","Location"] :
                    location_coordinate = coordinate_from_string(cell.coordinate)
                    location_col = location_coordinate[0]

                if cell.value in ["device","Device"] :
                    device_coordinate = coordinate_from_string(cell.coordinate)
                    device_col = device_coordinate[0]

                if cell.value in ["sub_device","Sub Device"] :
                    sub_device_coordinate = coordinate_from_string(cell.coordinate)
                    sub_device_col = sub_device_coordinate[0]

                if cell.value in ["model","Model", "Description","Model Name"] :
                    model_coordinate = coordinate_from_string(cell.coordinate)
                    model_col = model_coordinate[0]

                if cell.value in ["Model ID"] :
                    model_id_coordinate = coordinate_from_string(cell.coordinate)
                    model_id_col = model_id_coordinate[0]

                if cell.value in ["brand","Brand"] :
                    brand_coordinate = coordinate_from_string(cell.coordinate)
                    brand_col = brand_coordinate[0]

                if cell.value in ["purchase_month","Purchase Date"] :
                    purchase_month_coordinate = coordinate_from_string(cell.coordinate)
                    purchase_month_col = purchase_month_coordinate[0]

                if cell.value in ["first_name","First Name", "Customer Name"] :
                    first_name_coordinate = coordinate_from_string(cell.coordinate)
                    first_name_col = first_name_coordinate[0]

                if cell.value in ["last_name","Last Name"] :
                    last_name_coordinate = coordinate_from_string(cell.coordinate)
                    last_name_col = last_name_coordinate[0]

                if cell.value in ["email","Email ID"] :
                    email_coordinate = coordinate_from_string(cell.coordinate)
                    email_col = email_coordinate[0]

                if cell.value in ["mobile_number","Mobile Number"] :
                    mobile_number_coordinate = coordinate_from_string(cell.coordinate)
                    mobile_number_col = mobile_number_coordinate[0]

                if cell.value in ["imei_serial_no","Imei / Serial Nuber","IMEI Number"] :
                    imei_serial_no_coordinate = coordinate_from_string(cell.coordinate)
                    imei_serial_no_col = imei_serial_no_coordinate[0]

                if cell.value in ["term_type","Term Type"] :
                    term_type_coordinate = coordinate_from_string(cell.coordinate)
                    term_type_col = term_type_coordinate[0]

                if cell.value in ["device_value","Device Value"] :
                    invoice_value_coordinate = coordinate_from_string(cell.coordinate)
                    invoice_value_col = invoice_value_coordinate[0]

                if cell.value in ["device_currency","Device Currency"] :
                    device_currency_coordinate = coordinate_from_string(cell.coordinate)
                    device_currency_col = device_currency_coordinate[0]
                    print('device_currency_coordinate:: ',device_currency_coordinate)

                if cell.value in ["Plan Activation Date","Date"] : # there is no field named Date or plan activation date in excel
                    plan_ativation_date_coordinate = coordinate_from_string(cell.coordinate)
                    plan_ativation_date_col = plan_ativation_date_coordinate[0]
                logger.debug('before calling device name from excel file')

                if cell.value in ["Device Name"] :
                    logger.debug('inside if of checkin device name')
                    device_name_coordinate = coordinate_from_string(cell.coordinate)
                    device_name_col = device_name_coordinate[0]
                logger.debug('before calling plan price from excel file')

                if cell.value in ["Plan Price"] :
                    logger.debug('inside if of checkin plan price')

                    plan_price_coordinate = coordinate_from_string(cell.coordinate)
                    plan_price_col = plan_price_coordinate[0]

                if cell.value in ["Plan Tax"] :
                    plan_tax_coordinate = coordinate_from_string(cell.coordinate)
                    plan_tax_col = plan_tax_coordinate[0]

                if cell.value in ["Plan Total Price"] :
                    plan_total_price_coordinate = coordinate_from_string(cell.coordinate)
                    plan_total_price_col = plan_total_price_coordinate[0]

            if 'device_currency_col' in locals():
                device_currency_cell = "{}{}".format(device_currency_col, row_number )
                device_currency_value =  str(worksheet[device_currency_cell].value)

            if 'invoice_value_col' in locals():
                invoice_value_cell = "{}{}".format(invoice_value_col, row_number )
                invoice_value_value =  str(worksheet[invoice_value_cell].value)

            if 'location_col' in locals():
                location_value_cell = "{}{}".format(location_col, row_number )
                location_value =  str(worksheet[location_value_cell].value)

            if 'term_type_col' in locals():
                term_type_cell = "{}{}".format(term_type_col, row_number )
                term_type_value =  str(worksheet[term_type_cell].value)

            if 'imei_serial_no_col' in locals():
                imei_serial_no_cell = "{}{}".format(imei_serial_no_col, row_number )
                imei_serial_no_value =  str(worksheet[imei_serial_no_cell].value)

            if 'mobile_number_col' in locals():
                mobile_number_cell = "{}{}".format(mobile_number_col, row_number )
                mobile_number_value =  str(worksheet[mobile_number_cell].value)

            if 'email_col' in locals():
                email_cell = "{}{}".format(email_col, row_number )
                email_value =  str(worksheet[email_cell].value)

            if 'last_name_col' in locals():
                last_name_cell = "{}{}".format(last_name_col, row_number )
                last_name_value =  str(worksheet[last_name_cell].value)

            if 'first_name_col' in locals():
                first_name_cell = "{}{}".format(first_name_col, row_number )
                first_name_value =  str(worksheet[first_name_cell].value)

            if 'purchase_month_col' in locals():
                purchase_month_cell = "{}{}".format(purchase_month_col, row_number )
                purchase_month_value =  str(worksheet[purchase_month_cell].value)

            if 'model_col' in locals():
                model_cell = "{}{}".format(model_col, row_number )
                model_value =  str(worksheet[model_cell].value)

            if 'model_id_col' in locals():
                model_id_cell = "{}{}".format(model_id_col, row_number)
                model_code_value =  str(worksheet[model_id_cell].value)

            if 'device_col' in locals():
                device_cell = "{}{}".format(device_col, row_number )
                device_value =  str(worksheet[device_cell].value)

            if 'sub_device_col' in locals():
                sub_device_cell = "{}{}".format(sub_device_col, row_number )
                sub_device_value =  str(worksheet[sub_device_cell].value)

            if 'invoice_no_col' in locals():
                invoice_no_cell = "{}{}".format(invoice_no_col, row_number )
                invoice_no_value =  str(worksheet[invoice_no_cell].value)

            if 'sku_col' in locals():
                sku_cell = "{}{}".format(sku_col, row_number )
                sku_value =  str(worksheet[sku_cell].value)

            if 'brand_col' in locals():
                brand_cell = "{}{}".format(brand_col, row_number )
                brand_value =  str(worksheet[brand_cell].value)
                print ("yyyyyyyyyyyyyy- brand_value", brand_value)


            if 'plan_ativation_date_col' in locals():
                plan_ativation_date_cell = "{}{}".format(plan_ativation_date_col, row_number )
                plan_ativation_date_value =  str(worksheet[plan_ativation_date_cell].value)
                logger.debug("yyyyyyyyyyyyyy- plan_ativation_date_value", plan_ativation_date_value)


            if 'device_name_col' in locals():
                device_name_cell = "{}{}".format(device_name_col, row_number )
                device_name_value =  str(worksheet[device_name_cell].value)


            if 'plan_price_col' in locals():
                logger.debug ('yeeeeeeeeeeeeszzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
                plan_price_cell = "{}{}".format(plan_price_col, row_number )
                plan_price_value =  str(worksheet[plan_price_cell].value)
                logger.debug ("yyyyyyyyyyyyyy- plan_price_value", plan_price_value)

            if 'plan_tax_col' in locals():
                plan_tax_cell = "{}{}".format(plan_tax_col, row_number )
                plan_tax_value =  str(worksheet[plan_tax_cell].value)
                logger.debug ("yyyyyyyyyyyyyy- plan_tax_value", plan_tax_value)

            if 'plan_total_price_col' in locals():
                plan_total_price_cell = "{}{}".format(plan_total_price_col, row_number )
                plan_total_price_value =  str(worksheet[plan_total_price_cell].value)

            if row_number != 1 and partner_code in ['1026','1030','1031', '1025', '1014', '1031','1033','1035'] and email_value != 'None':
                print("inside")
                sku_value = sku_value if sku_value is not None and sku_value != "None" else ""
                PartnersDAO.insert_partners_offline_policy_data({
                    'popd_partner_code':partner_code,
                    'popd_invoice_no': invoice_no_value if 'invoice_no_value' in locals() else '',
                    'popd_invoice_value':invoice_value_value if 'invoice_value_value' in locals() else '',
                    'popd_plan_price':plan_price_value if 'plan_price_value' in locals() else '',
                    # 'popd_plan_price':'12',
                    'popd_plan_tax':plan_tax_value if 'plan_tax_value' in locals() else '',
                    # 'popd_plan_tax':"0",
                    'popd_plan_total_price':plan_total_price_value if 'plan_total_price_value' in locals() else '',
                    # 'popd_plan_total_price':'12',
                    'popd_sku':sku_value if 'sku_value' in locals() else '',
                    'popd_location': location_value if 'location_value' in locals() else '',
                    'popd_device':device_value if 'device_value' in locals() else '',
                    'popd_device_name':device_name_value if 'device_name_value' in locals() else '',
                    'popd_sub_device': sub_device_value if 'sub_device_value' in locals() else '',
                    'popd_brand':brand_value if 'brand_value' in locals() else '',
                    'popd_model':model_value if 'model_value' in locals() else '',
                    'popd_model_code':model_code_value if 'model_code_value' in locals() else '',
                    'popd_purchase_month':purchase_month_value if 'purchase_month_value' in locals() else '',
                    'popd_first_name':first_name_value if 'first_name_value' in locals() else '',
                    'popd_last_name':last_name_value if 'last_name_value' in locals() else '',
                    'popd_email':email_value if 'email_value' in locals() else '',
                    'popd_mobile_number':mobile_number_value if 'mobile_number_value' in locals() else '',
                    'popd_imei_serial_no':imei_serial_no_value if 'imei_serial_no_value' in locals() else '',
                    'popd_term_type':term_type_value if 'term_type_value' in locals() else '',
                    'popd_device_currency':device_currency_value if 'device_currency_value' in locals() else '',
                    # 'popd_activation_date':'2021-07-16',
                    'popd_activation_date': plan_ativation_date_value if 'plan_ativation_date_value' in locals() else '',
                    })

            if row_number != 1 and partner_code in ['RG'] and imei_serial_no_value != 'None':

                    PartnersDAO.insert_partners_redington_policy_data({
                    'prpd_partner_code':partner_code,
                    'prpd_device_name': model_value if 'model_value' in locals() else '',
                    'prpd_imei_serial_no': imei_serial_no_value if 'imei_serial_no_value' in locals() else '',
                    'prpd_device': 'Mobile Phone',
                    'prpd_brand': 'APPLE',
                    'prpd_model': model_value if 'model_value' in locals() else '',
                    'prpd_capacity': '',
                    'prpd_part_sku': sku_value if 'sku_value' in locals() else '',
                    'prpd_retailer_name': first_name_value if 'first_name_value' in locals() else '',
                    'prpd_invoice_dt': plan_ativation_date_value if 'plan_ativation_date_value' in locals() else '',
                    })
        print ("Cell Values!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        messages.success(request, 'File Uploaded successfuly. Data will be processed')
    template_name = 'partners/upload_create_policy.html'
    partners_obj = PartnersDAO.get_partners(condition={'partners_status':'active'})
    #print('partners_obj:: ',partners_obj)
    context = {"partners_obj":partners_obj, 'partners_config':partners_config}
    return render(request, template_name, context)
