LOGGING = {
	'version':1,
	'disable_existing_loggers': False,
	'formatters':{
		'large':{
			'format':'%(asctime)s  %(levelname)s  %(process)d  %(pathname)s  %(funcName)s  %(lineno)d  %(message)s  '
		},
		'tiny':{
			'format':'%(asctime)s  %(message)s  '
		}
	},
	'handlers':{
	 	'file': {
            'level': 'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'when':'H',
			'interval':1,
            'formatter': 'large',
            'filename': 'logs/InfoLoggers.log'
        }
	},
	'loggers':{
		'': {
            'level': 'DEBUG',
            'handlers': ['file']
        }
	},
}
