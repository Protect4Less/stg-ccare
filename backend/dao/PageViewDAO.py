from django.db import models
from django.conf import settings
from django.db import connection
from decouple import config
import datetime
from datetime import datetime

class PageViewDAO(object):
	
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg

	def get_pageview_stats_data(request):
		
		cursor = connection.cursor()
		

		condition = "AND pg_cmp_id="+request['cmp_id'] if 'cmp_id' in request and request['cmp_id'] != 0 else '' 
		condition += "AND pg_prod_id="+request['prod_id'] if 'prod_id' in request and request['prod_id'] != 0 else '' 

		start_date = datetime.strptime(request['start_date'], '%m/%d/%Y').strftime("%Y-%m-%d") if 'start_date' in request and request['start_date'] is not None else datetime.now().strftime("%Y-%m-%d")
		
		
		end_date = datetime.strptime(request['end_date'], '%m/%d/%Y').strftime("%Y-%m-%d") if 'end_date' in request  and request['end_date'] is not None else datetime.now().strftime("%Y-%m-%d")

		print(start_date, "   ", end_date)
		#exit()

		click_date = "'"+datetime.strptime(request['start_date'], '%m/%d/%Y').strftime("%d/%b/%Y")+"-"+datetime.strptime(request['end_date'], '%m/%d/%Y').strftime("%d/%b/%Y")+"' Date" if 'start_date' in request and request['start_date'] is not None and 'end_date' in request  and request['end_date'] is not None and start_date != end_date else "'"+datetime.now().strftime("%d/%b/%Y")+"' Date"

		print(click_date)
		#exit()
		
		
		query = "SELECT "+click_date+",pg_cmp_id 'Source',pg_prod_id 'Prodid',pg_geo 'Prod_Geo', pg_adnetwork_name 'AdNetwork', pg_cmp_name 'CampaignName', pg_cmp_createdby 'CreatedBy', SUM(pg_device_type_mobile) 'Mobile', SUM(pg_device_type_desktop) 'Desktop', SUM(pg_device_type_invalid) 'invalidDevice', SUM(pg_device_type_tablet) 'Tablet', SUM(pg_device_model_ipnone) 'iPhone', SUM(pg_device_model_ipad) 'iPad',  SUM(pg_device_os_android)  'Android', SUM(pg_page_type_home) 'HomePage', SUM(pg_page_type_plan_create) 'CreatePlan', ROUND(pg_page_average_percentage/100,2)  'Precentage',  SUM(pg_page_type_user_register)  'Register',  SUM(pg_page_type_payment)  'Payment', SUM(pg_page_type_billing)  'Billing', SUM(pg_page_type_login) 'Login', SUM(pg_page_type_thankyou)  'Thankyou'  FROM pageview_data  WHERE pg_clicks_date > date_sub(CONVERT_TZ('"+start_date+"','+00:00','+04:00'),INTERVAL 1 DAY) AND pg_clicks_date < CONVERT_TZ('"+end_date+"','+00:00','+04:00') "+condition+" GROUP BY 1,2,3,4,5,6,7"
		print(query)
		#exit()
		print("************************",query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]


	def get_pageview_data(column='',condition=''):
		column = column if column else '*'		
		
		query = "SELECT DATE(pv_addedon) 'Date',pv_cmp_id 'Source',pv_p_id 'prodid',pv_geo 'prod_geo', adnetwork_name 'AdNetwork', 'CampaignName', 'CreatedBy', count(DISTINCT CASE WHEN lower(pv_device_type) like '%smartphone%' THEN pv_sessionid END) 'Mobile', count(DISTINCT CASE WHEN lower(pv_device_type) like '%desktop%' THEN pv_sessionid END) 'Desktop', count(DISTINCT CASE WHEN lower(pv_device_type) like '%bot%' or lower(pv_device_type) like '%phablet%' or (lower(pv_device_type) like '%unk:%'and lower(pv_device_type) not like '%unk:desktop%')  THEN pv_sessionid END) 'Invalid_Device_Type', count(DISTINCT CASE WHEN lower(pv_device_type) like '%tablet%' THEN pv_sessionid END) 'Tablet', count(DISTINCT CASE WHEN pv_device_model = 'iPhone' THEN pv_sessionid END) 'iPhone',  count(DISTINCT CASE WHEN pv_device_model = 'iPad' THEN pv_sessionid END) 'iPad', count(DISTINCT CASE WHEN pv_device_os = 'Android' THEN pv_sessionid END) 'Android', count(DISTINCT CASE WHEN pv_page_type = 'pages_home' THEN pv_sessionid END) 'HomePage', count(DISTINCT CASE WHEN pv_page_type = 'plan_create' THEN pv_sessionid END) 'CreatePlan', ROUND((count(DISTINCT CASE WHEN pv_page_type = 'plan_create' THEN pv_sessionid END))/(count(DISTINCT CASE WHEN pv_page_type = 'pages_home' THEN pv_sessionid END))*100,2) 'Precentage', count(DISTINCT CASE WHEN pv_page_type = 'user_register' THEN pv_sessionid END) 'Register', count(DISTINCT CASE WHEN pv_page_type = 'plan_payment' THEN pv_sessionid END) 'Payment', count(DISTINCT CASE WHEN  pv_tran_id !=0 THEN pv_sessionid END) 'Billing', count(DISTINCT CASE WHEN pv_page_type = 'user_login_view'THEN pv_sessionid END) 'Login', count(DISTINCT CASE WHEN pv_sub_id > 0 THEN pv_sessionid END) 'Thankyou'  FROM "+config('SITE_DB')+".pageview, "+config('SITE_DB')+".adnetwork,"+config('SITE_DB')+".campaign  WHERE DATE(pv_addedon) >= DATE_SUB(DATE_FORMAT(NOW(), '%Y-%m-%d'),INTERVAL 1 DAY) AND DATE(pv_addedon) <= DATE_FORMAT(NOW(), '%Y-%m-%d') AND pv_cmp_id > 1000 AND pv_cmp_id = cmp_id AND cmp_adnetwork_id = adnetwork_id AND pv_page_type in ('pages_home','plan_create','user_regis-ter','plan_payment','policy_create_policy','user_login_view','plan_payment_subscription') GROUP BY 1,2"



		print(query)
		cursor = connection.cursor()
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

		
	def insert_pageview_mis_data(data):
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
		
		query = "INSERT INTO `pageview_data` ("+column_keys+") VALUES ("+column_values+") ON DUPLICATE KEY UPDATE "+update_column_key_value
		print('columns_s_value*************************************************************',columns_s_value)
		print(query)
		cursor.execute(query,columns_s_value)
		return cursor.lastrowid


	def get_pageview_stats(column='',condition=''):
		'''
		sql_update_column = ""
		sql_condition = ""
		row = None
		
		error = "condition data are missing" if condition == "" else None

		if error is None:

			for k,v in condition.items():
				sql_condition += k+" "+(" IS NULL " if v is None else " = '"+str(v)+"'")+" AND "

			sql_condition = sql_condition[:-5]

			cursor = connection.cursor()
			cursor.execute("SELECT * FROM `transaction_log` WHERE "+sql_condition)

			columns = [col[0] for col in cursor.description]
			row =  [
				dict(zip(columns, row))
				for row in cursor.fetchall()
			]
		'''
		row = [
			{"cmp_id": 1001, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 10110, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 },
			{"cmp_id": 1002, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 1550, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 }, 
			{"cmp_id": 1003, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 13410, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 }, 
			{"cmp_id": 1004, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 10510, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 },
			{"cmp_id": 1005, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 157410, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 },
			{"cmp_id": 1006, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 10230, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 },
			{"cmp_id": 1007, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 1070, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 },
			{"cmp_id": 1008, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 101310, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 },
			{"cmp_id": 1009, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 1610, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 },
			{"cmp_id": 1010, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 175110, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 },
			{"cmp_id": 1011, "country": "UAE", "adnetwork": "TMT Default", "plan": "Daily", "category": "PHONE", "visits": 101310, "unique_visits": 454, "msisdn_count": 45, "unique_msisdn": 40, "telco": "ETISALAT", "call_to_action": 30, "success": 20, "pending": 5, "failed": 5, "call_to_action_percentage": 50, "policy_purchase_count": 10, "cost": 15, "cr": 25, "revenue": "800 AED", "pb_sent": 10, "cpa": 80 }
			]
		
		return row

		
