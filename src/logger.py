import logging
import datetime
import os

PATH = f'{os.path.dirname(__file__)}/log'
DEBUG = False


def get_logger(level='warning', debug=DEBUG):
    """
    根据日期自动切分日志
    :param level: 日志打印级别
    :param debug: 开启debug则日志打印到控制台
    :return: 日志打印对象
    """

    level = level.upper()
    level = getattr(logging, level)

    if not os.path.exists(PATH):
        os.makedirs(PATH)

    log_file = f'{PATH}/{datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")}.log'
    log_format = '%(asctime)s[%(levelname)s]: %(filename)s[%(lineno)d]: %(message)s'
    if debug:
        logging.basicConfig(level=level, format=log_format)
    else:
        logging.basicConfig(filename=log_file, level=level, format=log_format)
    logger = logging.getLogger()

    return logger
