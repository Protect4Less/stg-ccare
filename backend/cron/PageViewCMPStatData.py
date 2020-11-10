from django_cron import CronJobBase, Schedule
from django.db import connection
from backend.dao.PageViewDAO import PageViewDAO
import datetime
from decouple import config
from datetime import datetime

#backend.cron.TimweBahrainNotification.TimweBahrainNotification
#python manage.py runcrons backend.cron.PageViewCMPStatData.PageViewCMPStatData

class PageViewCMPStatData(CronJobBase):
	RUN_EVERY_MINS = 1 # every 24 hours
	ALLOW_PARALLEL_RUNS = True
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'mis.PageViewCMPStatData'    # a unique code
	
	def init(self):

		pageview_data = PageViewDAO.get_pageview_data(column='',condition='')
		error = "pageview_data is empty" if len(pageview_data) == 0 else None
		
		if error is None:
			print(pageview_data)
			for pageview in pageview_data:
				
				pageview_dic = {'pg_clicks_date': pageview['Date'], 'pg_cmp_id': pageview['Source'], 'pg_prod_id': pageview['prodid'], 'pg_geo': pageview['prod_geo'], 'pg_adnetwork_name': pageview['AdNetwork'], 'pg_cmp_name': pageview['CampaignName'], 'pg_cmp_createdby': pageview['CreatedBy'], 'pg_device_type_mobile': pageview['Mobile'], 'pg_device_type_desktop': pageview['Desktop'],'pg_device_type_invalid': pageview['Invalid_Device_Type'], 'pg_device_type_tablet': pageview['Tablet'], 'pg_device_model_ipnone': pageview['iPhone'], 'pg_device_model_ipad': pageview['iPad'], 'pg_device_os_android': pageview['Android'], 'pg_page_type_home': pageview['HomePage'], 'pg_page_type_plan_create': pageview['CreatePlan'], 'pg_page_average_percentage': pageview['Precentage'] if pageview['Precentage'] is not None else 0 , 'pg_page_type_user_register': pageview['Register'], 'pg_page_type_payment': pageview['Payment'], 'pg_page_type_billing': pageview['Billing'], 'pg_page_type_login': pageview['Login'], 'pg_page_type_thankyou': pageview['Thankyou']}
				PageViewDAO.insert_pageview_mis_data(pageview_dic)

				pageview_dic={}
				
obj = PageViewCMPStatData()

obj.init()
