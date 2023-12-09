logs_conf =  { 
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'standard': { 
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] [%(lineno)s]: %(message)s'
        },
    },
    'handlers': { 
        'console': { 
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout', 
        },
    },
    'loggers': { 
        'src.gui': { 
            'handlers': [
                'console'
            ],
            'level': 'DEBUG',
            'propagate': False
        },
        'src.db': { 
            'handlers': [
                'console'
            ],
            'level': 'DEBUG',
            'propagate': False
        },
        '__main__': { 
            'handlers': [
                'console'
            ],
            'level': 'DEBUG',
            'propagate': False
        },
    } 
}