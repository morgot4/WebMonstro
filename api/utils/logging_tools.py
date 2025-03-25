import logging
from colorama import Fore, Style
from elasticsearch import Elasticsearch
import datetime

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        return not any(word in record.getMessage().lower() for word in ["password", "token", "secret"])
    

class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        if record.levelno in self.COLORS:
            record.levelname = (f"{self.COLORS[record.levelno]}"
                                f"{record.levelname}{Style.RESET_ALL}")
            record.msg = (f"{self.COLORS[record.levelno]}"
                          f"{record.msg}{Style.RESET_ALL}")
        return super().format(record)
    

class ElasticsearchHandler(logging.Handler):
    def __init__(self, host='localhost', index_name='app-logs'):
        super().__init__()
        self.es = Elasticsearch([host])
        self.index_name = index_name

    def emit(self, record):
        try:
            log_entry = {
                'timestamp': datetime.datetime.now(datetime.timezone.utc),
                'level': record.levelname,
                'message': record.getMessage(),
                'module': record.module
            }
        except Exception as e:
            print(e)