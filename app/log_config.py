import logging.config 
import logging
from datetime import datetime
from gunicorn import glogging

logger = logging.getLogger(__name__)
time_name = datetime.now().strftime('%Y%m%d_%H%M%S')

logging_cfg = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'KeyValueFormatter': {
            'format': (
                'timestamp=%(asctime)s pid=%(process)d '
                'loglevel=%(levelname)s msg=%(message)s'
            )
        },
    },
    'handlers': {
        "default_console": {
            "formatter": "KeyValueFormatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "error_console": {
            "formatter": "KeyValueFormatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access_console": {
            "formatter": "KeyValueFormatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "default_file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "KeyValueFormatter",
            "filename": f"app/logger/debug_{time_name}.log",
            "encoding": "utf8"
        },
        "error_file": {
            "formatter": "KeyValueFormatter",
            "class": "logging.FileHandler",
            "filename": f"app/logger/error_{time_name}.log",
        },
        "access_file": {
            "formatter": "KeyValueFormatter",
            "class": "logging.FileHandler",
            "filename": f"app/logger/access_{time_name}.log",
        },
    },
    'loggers': {
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["error_console", "error_file"],
            "propagate": False,
            "qualname": "gunicorn.error"
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["access_console", "access_file"],
            "propagate": False,
            "qualname": "gunicorn.access"
        },
        "gunicorn.mylog": {
            "level": "INFO",
            "handlers": ["default_console", "default_file"],
            "propagate": False,
            "qualname": "gunicorn.mylog"
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['default_console', "default_file"],
    }
}

def configure_logging():
    logging.config.dictConfig(logging_cfg)

class UniformLogger(glogging.Logger):

    def setup(self, cfg):
        configure_logging()
        