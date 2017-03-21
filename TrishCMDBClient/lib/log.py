# __Author__:oliver
# __DATE__:3/9/17
import logging
import os
from config import settings


class Logger(object):
    __instance = None

    def __init__(self):
        self.run_log_path = settings.LOG_FILE_PATH['run_log']
        self.error_log_path = settings.LOG_FILE_PATH['error_log']
        self.run_logger = None
        self.error_logger = None
        self.create_run_log()
        self.create_error_log()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    @staticmethod
    def check_path(file_path):
        log_dir = os.path.split(file_path)[0]   # /home/oliver/04 PycharmProjects/TrishCMDBClient/log
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

    def create_run_log(self):
        self.check_path(self.run_log_path)
        file_1_1 = logging.FileHandler(self.run_log_path, 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(levelname)s :  %(message)s")
        file_1_1.setFormatter(fmt)
        logger1 = logging.Logger('run_log', level=logging.INFO)
        logger1.addHandler(file_1_1)
        self.run_logger = logger1

    def create_error_log(self):
        self.check_path(self.error_log_path)
        file_1_1 = logging.FileHandler(self.error_log_path, 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s  - %(levelname)s :  %(message)s")
        file_1_1.setFormatter(fmt)
        logger1 = logging.Logger('run_log', level=logging.ERROR)
        logger1.addHandler(file_1_1)
        self.error_logger = logger1



    def log(self, message, mode=True):
        """
        写日志
        :param message: 日志信息
        :param mode: True表示运行日志，False表示错误日志
        :return:
        """
        print(message)
        if mode:
            self.run_logger.info(message)
        else:
            self.error_logger.error(message)


if __name__ == '__main__':
    log_dir = os.path.split(settings.LOG_FILE_PATH['run_log'])[0]
    print(log_dir)