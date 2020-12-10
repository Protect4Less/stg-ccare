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

	def insert_partners_offline_policy_data(data):
		inserted_id = ""
		columns_s_value = []
		cursor = connection.cursor()
		column_keys = ""
		column_values = ""
		for k,v in data.items():
			if k:
				column_keys += k+", "
				column_values += "%s,"
				columns_s_value.append(str(v))
			
		column_keys += "popd_addedon"
		column_values += "NOW()"
		query = "INSERT INTO "+config('SITE_DB')+".`partners_offline_policy_data` ("+column_keys+") VALUES ("+column_values+")"
		print(query)

		cursor.execute(query,columns_s_value)
		inserted_id = cursor.lastrowid

		return inserted_id