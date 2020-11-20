import os

from dotenv import load_dotenv

load_dotenv()
os.makedirs(os.getenv('LOG_STORAGE'), exist_ok=True)


LOGGER_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'error': {
            'format': '%(levelname)s <PID %(process)d:%(processName)s> %(name)s.%(funcName)s(): %(message)s'
        }
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard'
        },

        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': f'{os.getenv("BACKUP_STORAGE")}/info.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 20,
            'encoding': 'utf8'
        }
    },

    'loggers': {
        'main': {
            'level': 'INFO',
            'handlers': [
                'console',
                'file_handler',
            ],
            'propagate': 'no'
        }
    }
}

