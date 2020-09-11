import logging
import logging.config
import yaml
from config.application_config import API_LOG
from config.application_config import LOG_FILE_CONFIG


class Logger:
    def __init__(self):
        with open(LOG_FILE_CONFIG, 'rt') as file:
            config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)

    def get_logger(self, log_name):
        new_logger = logging.getLogger(log_name)
        return new_logger


api_logger = Logger().get_logger(API_LOG)
