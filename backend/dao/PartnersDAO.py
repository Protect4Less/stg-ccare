from django.db import models
from django.conf import settings
from django.db import connection
from decouple import config
from dateutil.relativedelta import relativedelta

import datetime
from datetime import datetime

class PartnersDAO(object):
	
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg

	def get_partners(column='',condition=''):
		sql_condition = ""
		if len(condition) > 0:
			for k,v in condition.items():
				if "#" in k:
					column_name, column_condition = k.split("#")
					if(column_condition == "IN"):
						sql_condition += column_name+" "+column_condition+" ("+str(v)+") AND "
					else:	
						sql_condition += column_name+" "+column_condition+" "+str(v)+" AND "
				else:
					sql_condition += k+" "+(" IS NULL " if v is None else " = '"+str(v)+"'")+" AND "

			sql_condition = sql_condition[:-5]
			query = "SELECT * FROM "+config('SITE_DB')+".`partners` WHERE "+sql_condition
		else:
			query = "SELECT * FROM "+config('SITE_DB')+".`partners` ORDER BY 1 DESC LIMIT 1000"

		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_commission(geo = '', user_id = '', make = '', category = '', plan = '', start_date='', end_date=''):
		print("get_commission called")
		sql_condition = ''
		category_table = config('SITE_DB')+'.category'
		partners_table = config('SITE_DB')+'.partners'
		partners_commission_table = config('SITE_DB')+'.partners_commission'

		#sql_condition += "ps_mis_user_id = "+str(user_id)+" AND " if user_id !='' else "ps_mis_user_id = 0 AND "

		#sql_condition += "ps_cat_id = "+str(category_id)+" AND " if category_id !='' else ""

		#sql_condition += "ps_plan = '"+plan+"' AND " if plan !='' else ""

		#sql_condition += "ps_date >= CURDATE() AND " if start_date == '' and end_date == '' else " (ps_date >= '"+start_date+"' AND ps_date < DATE_ADD('"+end_date+"', INTERVAL 1 DAY)) AND "

		sql_condition = sql_condition[:-5]

		query = "SELECT  \n"\
			"DATE(pc_sub_date) pc_sub_date,\n"\
			"(SELECT partner_company_name FROM "+partners_table+" WHERE partners_id = pc_partners_id ) partner_name,\n"\
			"pc_geo,\n"\
			"(select cat_name FROM "+category_table+" WHERE cat_id = pc_cat_id) category_name,\n"\
			"pc_make_name,\n"\
			"pc_item_name,\n"\
			"pc_plan,\n"\
			"SUM(pc_amount) pc_amount\n"\
			""+sql_condition+"\n"\
			"FROM "+partners_commission_table+"\n"\
			"GROUP BY 1,2,3,4,5,6,7 \n "\
			"ORDER BY 1 DESC "

		print(query)
		cursor = connection.cursor()
		
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]


	def update_partners(column='',condition=''):
		sql_update_column = ""
		sql_condition = ""
		row = ""
		error = "update date are missing" if column == "" else None
		error = error if error is not None else "condition are missing" if condition == "" else None

		if error is None:

			for k,v in column.items():
				sql_update_column += k+"='"+str(v)+"',"

			sql_update_column += "partners_updatedon = NOW()"

			for k,v in condition.items():
				sql_condition += k+" "+(" IS NULL " if v is None else " = '"+str(v)+"'")+" AND "

			sql_condition = sql_condition[:-5]

			cursor = connection.cursor()
			query = "UPDATE "+config('SITE_DB')+".`partners` SET "+sql_update_column+" WHERE "+sql_condition
			print(query)			
			row = cursor.execute(query)

		return row
	
	def get_patnersub_data(column='',condition=''):
		column = column if column else '*'

		res  = ", ".join(["'{}'".format(x) for x in settings.SKIP_EMAIL])
    

		query = "SELECT DATE(s_sub_date) 'sub_date', (select p.partner_company_name from "+config('SITE_DB')+".partners p where p.partners_code = s.s_partner_code) PartnerName, s_partner_code PartnerCode, COUNT(1) TotalSubs, SUM(if(s_plan = 'monthly',1,0)) 'MonthlySubs', SUM(if(s_plan = 'yearly',1,0)) 'YearlySubs', SUM(if(s_plan = 'monthly',s_acq_rev,0)) MonthlyAcqRev, SUM(if(s_plan = 'yearly',s_acq_rev,0)) YearlyAcqRev, SUM(s_acq_rev) 'acq_rev', s_price_unit FROM "+config('SITE_DB')+".subscription s WHERE DATE(s_sub_date) >= DATE_SUB(DATE_FORMAT(NOW(), '%Y-%m-%d'),INTERVAL 1 DAY) AND s.s_partner_code != '' AND s.s_emailid not in ("+res+") AND s.s_billing_emailid not in ("+res+") GROUP BY 1,2,3,10 "

		print(query)
		cursor = connection.cursor()
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def insert_partner_subscription_mis_data(data):
		inserted_id = ""
		columns_s_value = []
		update_column_key_value = ''
		cursor = connection.cursor()
		column_keys = ""
		column_values = ""
		for k,v in data.items():
			if k:
				column_keys += k+", "
				column_values += "%s,"
				columns_s_value.append(str(v))
				update_column_key_value += k+"= '"+ str(v)+"',"

		update_column_key_value = update_column_key_value.rstrip(', ')
		column_keys = column_keys.rstrip(', ')
		column_values = column_values.rstrip(',')
		
		query = "INSERT INTO `partner_subscription_data` ("+column_keys+") VALUES ("+column_values+") ON DUPLICATE KEY UPDATE "+update_column_key_value
		print('columns_s_value*************************************************************',columns_s_value)
		print(query)
		cursor.execute(query,columns_s_value)
		return cursor.lastrowid

	def get_partner_stats_data(request):
		
		cursor = connection.cursor()
		

		condition = ''
		start_date = datetime.strptime(request['start_date'], '%m/%d/%Y').strftime("%Y-%m-%d") if 'start_date' in request and request['start_date'] is not None else datetime.now().strftime("%Y-%m-%d")
		
		
		end_date = datetime.strptime(request['end_date'], '%m/%d/%Y').strftime("%Y-%m-%d") if 'end_date' in request  and request['end_date'] is not None else datetime.now().strftime("%Y-%m-%d")
		
		sub_date = "'"+datetime.strptime(request['start_date'], '%m/%d/%Y').strftime("%d/%b/%Y")+"-"+datetime.strptime(request['end_date'], '%m/%d/%Y').strftime("%d/%b/%Y")+"' sub_date" if 'start_date' in request and request['start_date'] is not None and 'end_date' in request  and request['end_date'] is not None and start_date != end_date else "'"+datetime.now().strftime("%d/%b/%Y")+"' sub_date"

		query = "SELECT "+sub_date+",psd_partner_code 'PartnerCode', psd_partner_name 'PartnerName', SUM(psd_total_sub) 'TotalSubs', SUM(psd_total_sub_monthly) 'MonthlySubs', SUM(psd_total_sub_yearly) 'YearlySubs', ROUND(SUM(psd_total_acqrev),2) 'acq_rev', ROUND(SUM(psd_total_acqrev_monthly),2) 'MonthlyAcqRev', ROUND(SUM(psd_total_acqrev_yearly),2) 'YearlyAcqRev', psd_price_unit 's_price_unit'  FROM partner_subscription_data  WHERE psd_sub_date >= '"+start_date+"' AND psd_sub_date <= '"+end_date+"' "+condition+" GROUP BY 1,2,3,10"
		print("************************",query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]	
