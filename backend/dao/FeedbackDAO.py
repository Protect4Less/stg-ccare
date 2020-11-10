from django.db import models
from django.conf import settings
from django.db import connection
from decouple import config

class FeedbackDAO():

	def get_policy_feeback_feeling_count():
		query = "SELECT pfs_feeling, count(pfs_count) feeling_count FROM "+config('SITE_DB')+".`policy_feedback_summary` GROUP BY 1 "
		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def get_policy_feeback_summary():
		query = "SELECT pfs_feeling, IF(pfs_pfm_id IS NOT NULL AND pfs_pfm_id > 0, (SELECT pfm_name FROM "+config('SITE_DB')+".`policy_feedback_master` WHERE pfm_id = pfs_pfm_id), '') pfs_pfm_id, SUM(pfs_count) pfs_count FROM "+config('SITE_DB')+".`policy_feedback_summary` GROUP BY 1,2 "
		cursor = connection.cursor()
		print(query)
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		#print(columns)
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

