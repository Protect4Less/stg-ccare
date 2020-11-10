from django.db import models
from django.conf import settings
from django.db import connection
from decouple import config

class CommonDAO():

	def get_country():
		query = "SELECT * FROM "+config('SITE_DB')+".`country` where country_status='active'"
		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_category():
		query = "SELECT * FROM "+config('SITE_DB')+".`category`"
		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	# def get_payment_method():
	# 	query = "SELECT * FROM "+config('SITE_DB')+".`payment_method`"
	# 	cursor = connection.cursor()
	# 	print(query)
	# 	cursor.execute(query)
	# 	columns = [col[0] for col in cursor.description]
	# 	#print(columns)
	# 	return [
	# 		dict(zip(columns, row))
	# 		for row in cursor.fetchall()
	# 	]

	# def get_payment_partner():
	# 	query = "SELECT * FROM "+config('SITE_DB')+".`payment_partner`"
	# 	cursor = connection.cursor()
	# 	print(query)
	# 	cursor.execute(query)
	# 	columns = [col[0] for col in cursor.description]
	# 	#print(columns)
	# 	return [
	# 		dict(zip(columns, row))
	# 		for row in cursor.fetchall()
	# 	]

	def get_brand():
		query = "SELECT * FROM "+config('SITE_DB')+".`make`"
		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_plan():
		query = "SELECT distinct(plan_type) FROM "+config('SITE_DB')+".`plan`"
		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_date():
		query = "SELECT * FROM "+config('SITE_DB')+".`plan`"
		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]
	#Added for getting product

	def get_product(column='',condition=''):
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
			query = "SELECT * FROM "+config('SITE_DB')+".`product` WHERE "+sql_condition
		else:
			query = "SELECT * FROM "+config('SITE_DB')+".`product` ORDER BY 1 DESC LIMIT 1000"

		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	#Added for getting category

	def get_category(column='',condition=''):
		print("get_category")
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
			query = "SELECT * FROM "+config('SITE_DB')+".`category` WHERE "+sql_condition
		else:
			query = "SELECT * FROM "+config('SITE_DB')+".`category`"

		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_payment_method(column='',condition=''):
		print("get_payment")
		sql_condition = ""
		if len(condition) > 0:
			for k,v in condition.items():
				if "#" in k:
					column_name, column_condition = k.split("#")
					if(column_condition == "IN"):
						sql_condition += column_name+" "+column_condition+" ("+str(v)+") AND "
					elif(column_condition == "FIND_IN_SET"):	
						sql_condition += str(v)+" AND "
					else:	
						sql_condition += column_name+" "+column_condition+" "+str(v)+" AND "
				else:
					sql_condition += k+" "+(" IS NULL " if v is None else " = '"+str(v)+"'")+" AND "

			sql_condition = sql_condition[:-5]
			query = "SELECT * FROM "+config('SITE_DB')+".`payment_method` WHERE "+sql_condition
			print("if Query---> ",query)
		else:
			query = "SELECT * FROM "+config('SITE_DB')+".`payment_method`"
			print("else Query---> ",query)

		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_payment_partner(column='',condition=''):
		print("get_payment")
		sql_condition = ""
		if len(condition) > 0:
			for k,v in condition.items():
				if "#" in k:
					column_name, column_condition = k.split("#")
					if(column_condition == "IN"):
						sql_condition += column_name+" "+column_condition+" ("+str(v)+") AND "
					elif(column_condition == "FIND_IN_SET"):	
						sql_condition += str(v)+" AND "
					else:	
						sql_condition += column_name+" "+column_condition+" "+str(v)+" AND "
				else:
					sql_condition += k+" "+(" IS NULL " if v is None else " = '"+str(v)+"'")+" AND "

			sql_condition = sql_condition[:-5]
			query = "SELECT * FROM "+config('SITE_DB')+".`payment_partner` WHERE "+sql_condition
		else:
			query = "SELECT * FROM "+config('SITE_DB')+".`payment_partner`"

		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_template(column='', condition=''):
		query = "SELECT * FROM "+config('SITE_DB')+".`template`"
		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_adnetwork():
		query = "SELECT * FROM "+config('SITE_DB')+".`adnetwork`"
		cursor = connection.cursor()
		print(query)

		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	print("succeesful")

	# def  get_product(country=''):
	# 	query = "SELECT * FROM "+config('SITE_DB')+".`product` where prod_id "
	# 	cursor = connection.cursor()
	# 	print(query)
	# 	cursor.execute(query)
	# 	columns = [col[0] for col in cursor.description]
	# 	#print(columns)
	# 	return [
	# 		dict(zip(columns, row))
	# 		for row in cursor.fetchall()
	# 	]

