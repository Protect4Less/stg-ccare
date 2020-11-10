from django.db import models
from django.conf import settings
from django.db import connection
from decouple import config

class MasterDAO(object):
	
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg

	def insert_adnetwork(data):
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
				
			column_keys += "adnetwork_addedon, adnetwork_updatedon"
			column_values += "NOW(), NOW()"
			query = "INSERT INTO "+config('SITE_DB')+".`adnetwork` ("+column_keys+") VALUES ("+column_values+")"
			cursor.execute(query)
			inserted_id = cursor.lastrowid

		return inserted_id

	def insert_email(data):
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
				
			column_keys += "et_addedon"
			column_values += "NOW()"
			query = "INSERT INTO "+config('SITE_DB')+".`email_transaction` ("+column_keys+") VALUES ("+column_values+")"
			print(query)
			cursor.execute(query)
			inserted_id = cursor.lastrowid

		return inserted_id

	def insert_mis_user(data):
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
				
			column_keys += "date_joined"
			column_values += "NOW()"
			query = "INSERT INTO "+config('PARTNER_DB')+".`auth_user` ("+column_keys+") VALUES ("+column_values+")"
			print(query)
			cursor.execute(query)
			inserted_id = cursor.lastrowid

		return inserted_id

	def save_campaign(country='', product=''):
		query = "SELECT * FROM "+config('SITE_DB')+".`country`"
		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_product(product):
		query = "SELECT * FROM "+config('SITE_DB')+".`product`"
		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]
