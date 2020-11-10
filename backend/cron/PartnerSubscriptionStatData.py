from django_cron import CronJobBase, Schedule
from django.db import connection
from backend.dao.PartnersDAO import PartnersDAO
import datetime
from decouple import config
from datetime import datetime


#python manage.py runcrons backend.cron.PartnerSubscriptionStatData.PartnerSubscriptionStatData

class PartnerSubscriptionStatData(CronJobBase):
	RUN_EVERY_MINS = 1 # every 24 hours
	ALLOW_PARALLEL_RUNS = True
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'mis.PartnerSubsciptionStatData'    # a unique code
	
	def init(self):

		patnersub_data = PartnersDAO.get_patnersub_data(column='',condition='')
		error = "patnersub_data is empty" if len(patnersub_data) == 0 else None
		
		if error is None:
			print(patnersub_data)
			for patnersub in patnersub_data:
				
				partner_dic = {'psd_sub_date': patnersub['sub_date'], 'psd_partner_name': patnersub['PartnerName'], 'psd_partner_code': patnersub['PartnerCode'], 'psd_total_sub': patnersub['TotalSubs'], 'psd_total_sub_monthly': patnersub['MonthlySubs'], 'psd_total_sub_yearly': patnersub['YearlySubs'], 'psd_total_acqrev': patnersub['acq_rev'], 'psd_total_acqrev_monthly': patnersub['MonthlyAcqRev'], 'psd_total_acqrev_yearly': patnersub['YearlyAcqRev'], 'psd_price_unit': patnersub['s_price_unit']}
				PartnersDAO.insert_partner_subscription_mis_data(partner_dic)

				partner_dic={}
				
obj = PartnerSubscriptionStatData()

obj.init()
