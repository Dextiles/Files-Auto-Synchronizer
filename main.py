from api.Yandex import YandexAPI
from File_synchronizer import Synchronizer
import logging
import threading
import os
from misc.instruments import load_config, check_directory


def loop(done_param, token, folder, directory, interval=1):
    while not done_param.wait(interval):
        Synchronizer(YandexAPI(token, folder), directory).synchronise()


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.mkdir('logs')

    logging.basicConfig(level=logging.INFO, filename='logs/logs.log', filemode='w', encoding='utf-8',
                        format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    config = load_config()
    check_directory(config['PARAMS']['local_folder'])
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
