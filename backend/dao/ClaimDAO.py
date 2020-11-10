from django.db import models
from django.conf import settings
from django.db import connection
from decouple import config
from dateutil.relativedelta import relativedelta

import datetime
from datetime import datetime

class ClaimDAO(object):
	
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg

	def get_claim_pending_payment(column='',condition=''):
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
			query = "SELECT * FROM "+config('SITE_DB')+".`claim_pending_payment` WHERE "+sql_condition
		else:
			query = "SELECT * FROM "+config('SITE_DB')+".`claim_pending_payment` ORDER BY 1 DESC LIMIT 1000"

		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	


	def update_claim_pending_payment(column='',condition=''):
		sql_update_column = ""
		sql_condition = ""
		row = ""
		error = "update date are missing" if column == "" else None
		error = error if error is not None else "condition are missing" if condition == "" else None

		if error is None:

			for k,v in column.items():
				sql_update_column += k+"='"+str(v)+"',"

			sql_update_column += "cpp_updatedon = NOW()"

			for k,v in condition.items():
				sql_condition += k+" "+(" IS NULL " if v is None else " = '"+str(v)+"'")+" AND "

			sql_condition = sql_condition[:-5]

			cursor = connection.cursor()
			query = "UPDATE "+config('SITE_DB')+".`claim_pending_payment` SET "+sql_update_column+" WHERE "+sql_condition
			print(query)			
			row = cursor.execute(query)

		return row
	
	