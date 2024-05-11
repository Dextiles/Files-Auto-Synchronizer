from api.Yandex import YandexAPI
from File_synchronizer import Synchronizer
import logging
import threading
import os
from exceptions.SystemExceptions import *
import configparser


def loop(done_param, token, folder, directory, interval=1):
    while not done_param.wait(interval):
        Synchronizer(YandexAPI(token, folder), directory).synchronise()


def load_config():
    try:
        if not os.path.exists('config.ini'):
            raise InIEmptyError
        else:
            cfg = configparser.ConfigParser()
            with open('config.ini') as cf:
                cfg.read_file(cf)
                if not cfg.has_section('PARAMS') or not cfg.has_section('SERVICE'):
                    raise NotGoodINIError
                else:
                    params = cfg.options('PARAMS')
                    service = cfg.options('SERVICE')
                    if 'local_folder' not in params and 'service_folder' not in params and 'sync_interval' not in params:
                        raise NotGoodINIError
                    elif 'service_token' not in service and 'service_type' not in service:
                        raise NotGoodINIError
    except Exception as ex:
        exit(f'Невозможно начать работу: {ex}')
    else:
        return cfg


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.mkdir('logs')

    logging.basicConfig(level=logging.INFO, filename='logs/logs.log', filemode='w', encoding='utf-8',
                        format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    config = load_config()
    done = threading.Event()
    logging.info('Запуск программы')
    logging.info(f'Директория для отслеживания: {config["PARAMS"]["local_folder"]}')
    logging.info(f'Директория для загрузки: {config["PARAMS"]["service_folder"]}')

    threading.Thread(target=loop, args=[done,
                                        config['SERVICE']['service_token'],
                                        config['PARAMS']['service_folder'],
                                        config['PARAMS']['local_folder'],
                                        int(config['PARAMS']['sync_interval'])], daemon=True).start()
    input('Press Enter to exit.')
    done.set()
