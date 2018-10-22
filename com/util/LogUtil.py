# coding=utf-8
import os
import datetime
import logging
import logging.config


class LogUtil:

    @staticmethod
    def main():
        """"""
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        LOG_DIR = os.path.join(BASE_DIR, "logs")
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)  # 创建路径

        LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
        print(LOG_FILE)

        LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {
                    'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
                },
                'standard': {
                    'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
                },
            },

            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout"
                },

                "default": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "INFO",
                    "formatter": "simple",
                    "filename": os.path.join(LOG_DIR, LOG_FILE),
                    'mode': 'w+',
                    "maxBytes": 1024 * 1024 * 5,  # 5 MB
                    "backupCount": 20,
                    "encoding": "utf8"
                },
            },

            # "loggers": {
            #     "app_name": {
            #         "level": "INFO",
            #         "handlers": ["console"],
            #         "propagate": "no"
            #     }
            # },

            "root": {
                'handlers': ['default'],
                'level': "INFO",
                'propagate': False
            }
        }

        logging.config.dictConfig(LOGGING)

    @staticmethod
    def getLog():
        LogUtil.main()
        return logging.getLogger(__file__)
