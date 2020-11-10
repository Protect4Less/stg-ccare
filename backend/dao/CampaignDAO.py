from django.db import models
from django.conf import settings
from django.db import connection
from decouple import config

class CampaignDAO(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg

	def insert_campaign(data):
		inserted_id = ""
		error = "data are missing" if data == "" else None

		if error is None:
			cursor = connection.cursor()
			column_keys = ""
			column_values = ""
			for k,v in data.items():
				if k:
					column_keys += k+", "
					column_values += "'"+str(v)+"', "
				
			column_keys += "cmp_addedon, cmp_updatedon"
			column_values += "NOW(), NOW()"
			query = "INSERT INTO "+config('SITE_DB')+".`campaign` ("+column_keys+") VALUES ("+column_values+")"
			print(query)
			cursor.execute(query)
			inserted_id = cursor.lastrowid

		return inserted_id

	def insert_campaign_meta(data):
		inserted_id = ""
		error = "data are missing" if data == "" else None

		if error is None:
			cursor = connection.cursor()
			column_keys = ""
			column_values = ""
			for k,v in data.items():
				if k:
					column_keys += k+", "
					column_values += "'"+str(v)+"', "
				
			column_keys += "cm_addedon, cm_updatedon"
			column_values += "NOW(), NOW()"
			query = "INSERT INTO "+config('SITE_DB')+".`campaign_meta` ("+column_keys+") VALUES ("+column_values+")"
			print(query)
			cursor.execute(query)
			inserted_id = cursor.lastrowid

		return inserted_id

	def get_campaign_stats(column='',condition=''):
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

	def save_campaign(data):

		inserted_id = ""
		error = "data are missing" if data == "" else None

		if error is None:
			cursor = connection.cursor()
			column_keys = ""
			column_values = ""
			for k,v in data.items():
				if k:
					column_keys += k+", "
					column_values += "'"+str(v)+"', "
				
			column_keys += "cmp_addedon, cmp_updatedon"
			column_values += "NOW(), NOW()"
			query = "INSERT INTO "+config('SITE_DB')+".`campaign` ("+column_keys+") VALUES ("+column_values+")"

			print(query)
			cursor.execute(query)
			inserted_id = cursor.lastrowid

		return inserted_id

		#print("I am in the same campaign")

		# query = "INSERT INTO "+config('SITE_DB')+".`campaign` (cmp_geo,cmp_p_id) values ('"+country+"','"+product+"')"

		# print(query)
		# cursor = connection.cursor()
		
		# cursor.execute(query)
		# return "saved successfully"
	def get_campaign_view_data(cmp_id):
		sql_condition = ''
		campaign_table = config('SITE_DB')+'.campaign'
		adnetwork_table = config('SITE_DB')+'.adnetwork'

		query = "SELECT  \n"\
				"cmp_id, \n"\
				"cmp_geo, \n"\
				"cmp_plan cmp_camp_plan, \n"\
				"(cmp_type) cmp_camp_type, \n"\
				"(cmp_pb_type) cmp_pb_type, \n"\
				"cmp_trail_days, \n"\
				"cmp_pb_type, \n"\
				"cmp_pb_percentage, \n"\
				"cmp_pb_cap, \n"\
				"cmp_sub_cap, \n"\
				"cmp_charge_cap, \n"\
				"(SELECT prod_geo from "+config('SITE_DB')+'.product'+" a where a.prod_id  = cmp.cmp_p_id) cmp_product, \n"\
				"(SELECT cat_name from "+config('SITE_DB')+'.category'+" b where b.cat_id  = cmp.cmp_cat_id) cmp_category, \n"\
				"(SELECT pm_name from "+config('SITE_DB')+'.payment_method'+" pay where pay.pm_id  = cmp.cmp_pm_ids) cmp_cat_p_method, \n"\
				"(SELECT pp_name from "+config('SITE_DB')+'.payment_partner'+" pay_part where pay_part.pp_id  = cmp.cmp_pp_ids) cmp_cat_p_partner, \n"\
				"(SELECT template_name from "+config('SITE_DB')+'.template'+" template where template.template_id  = cmp.cmp_template_id) cmp_template, \n"\
				"(SELECT adnetwork_name from "+config('SITE_DB')+'.adnetwork'+" adnet where adnet.adnetwork_id = cmp.cmp_adnetwork_id) cmp_adnet_id \n"\
				"FROM "+campaign_table+" as cmp"

		print(query)
		cursor = connection.cursor()
		
		cursor.execute(query)
		print("Execute successfully campaign List")
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_campaign_list():
		sql_condition = ''
		campaign_table = config('SITE_DB')+'.campaign'
		adnetwork_table = config('SITE_DB')+'.adnetwork'

		query = "SELECT  cmp_id, (SELECT adnetwork_name from "+adnetwork_table+" a where a.adnetwork_id  = b.cmp_adnetwork_id) cmp_adnetwork, cmp_geo, cmp_plan, cmp_adnetwork_type, TRIM(cmp_url) as cmp_url from "+campaign_table+" b where cmp_id > 1000"

		print(query)
		cursor = connection.cursor()
		
		cursor.execute(query)
		print("Execute successfully campaign List")
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

		# for update campaign
	def update_campaign(data,cmp_id=''):

		inserted_id = ""
		error = "data are missing" if data == "" else None

		if error is None:
			cursor = connection.cursor()
			column_keys = ""
			column_values = ""
			for k,v in data.items():
				if k:
					column_keys += k+"="+"'"+str(v)+"', "
					#column_values += "'"+str(v)+"', "
			column_keys += "cmp_addedon=NOW(), cmp_updatedon=NOW()"
			#print("column_keys====",column_keys)
			#column_values += "NOW(), NOW()"
			query = "update "+config('SITE_DB')+".`campaign` set "+column_keys+" where cmp_id="+cmp_id+" "
			#print("query-------------",query)
			cursor.execute(query)
			inserted_id = cursor.lastrowid

		return inserted_id

	
	def get_campaign_data(column='',condition=''):

		sql_condition = ""

		columns = column if column is not '' else '*' 

		if condition is not '':
			sql_condition = ' WHERE '
			for k,v in condition.items():
				if "#" in k:
					print('######################################################')
					column_name, column_condition = k.split("#")
					sql_condition += column_name+" "+column_condition+" "+str(v)+" AND "
				else:
					sql_condition += k+" "+(" IS NULL " if v is None else " = '"+str(v)+"'")+" AND "

			# for k,v in condition.items():
			# 	print('######################kkkkkkkkkkkkkkkkkkkk',k)
			# 	if "#" in k:
			# 		print('######################################################')
			# 		column_name, column_condition = k.split("#")
			# 		sql_condition += column_name+" "+column_condition+" "+str(v)+" AND "
			# 	elif "$" in k:
			# 		print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
			# 		column_name, column_condition = k.split("*")
			# 		sql_condition += column_condition+" "+str(v)+" AND "
			# 	else:
			# 		sql_condition += k+" "+(" IS NULL " if v is None else " = '"+str(v)+"'")+" AND "
		
		sql_condition = sql_condition[:-5]

		print("WHERE------------------------",sql_condition)
		# cursor = connection.cursor()


		# column = column if column else '*'
		# sql_condition = ""
		# for k,v in condition.items():
		# 	sql_condition += k+" "+(" IS NULL " if v is None else " = '"+str(v)+"'")+" AND "
		# sql_condition = sql_condition[:-5]

		campaign_table = config('SITE_DB')+'.campaign'
		query = "SELECT "+columns+" FROM "+campaign_table+" "+sql_condition
		print(query)
		cursor = connection.cursor()
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]


	def save_campaign_url(id='',url='',cmp_url=''):
		query = "update "+config('SITE_DB')+".`campaign` set "+cmp_url+"='"+url+"' where cmp_id="+id+" "
		# query = "update "+config('SITE_DB')+".`campaign` set "+cmp_step1_url+"='"+url+"' where cmp_id="+id+" "

		print(query)
		cursor = connection.cursor()
		cursor.execute(query)
		inserted_id = cursor.lastrowid

		return inserted_id

	def save_campaign_json(cmp_plan_text_json='',id=''):
		print("inside json")
		query = "update "+config('SITE_DB')+".`campaign` set cmp_plan_text_json="+cmp_plan_text_json+" where cmp_id="+id+" "
		# query = "update "+config('SITE_DB')+".`campaign` set "+cmp_step1_url+"='"+url+"' where cmp_id="+id+" "

		print(query)
		cursor = connection.cursor()
		cursor.execute(query)
		inserted_id = cursor.lastrowid

		return inserted_id	


	def get_prepopulate_list(id=''):
		sql_condition = ''
		campaign_table = config('SITE_DB')+'.campaign'

		query = "SELECT  cmp_geo,cmp_p_id,cmp_cat_id,cmp_pm_ids, cmp_pp_ids, cmp_plan, cmp_template_id, cmp_adnetwork_id, cmp_type, cmp_adnetwork_type, cmp_trail_days, cmp_pb_type, cmp_charge_cap, cmp_pb_cap, cmp_pb_percentage, cmp_sub_cap from "+campaign_table+" where cmp_id="+id+" " 

		print(query)
		cursor = connection.cursor()
		
		cursor.execute(query)
		print("Execute successfully get_prepopulate_list")
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]	
