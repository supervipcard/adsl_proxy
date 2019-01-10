# -*- coding: utf-8 -*-

import requests
import subprocess
import time
import json
from settings import *
import logging
import logging.handlers


# 动态VPS
class ADSLProxy(object):
    @staticmethod
    def change():
        while True:
            try:
                (status, output) = subprocess.getstatusoutput(CMD)
                if status == 0 and 'Connected!' in output:
                    return True
            except Exception as e:
                print(e)
            time.sleep(SLEEP_TIME)

    @classmethod
    def send_and_get_ip(cls):
        while True:
            try:
                response = requests.post(url=VERIFY_URL, data={'token': TOKEN, 'port': PROXY_P0RT, 'channel': PROXY_CHANNEL}, timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    res = json.loads(response.text)
                    logger.info(str(res))
                    if res['sign']:
                        return True
            except Exception as e:
                print(e)
            cls.change()
            time.sleep(SLEEP_TIME)

    @classmethod
    def pre_notify(cls):
        while True:
            try:
                response = requests.post(url=NOTIFY_URL, data={'token': TOKEN, 'channel': PROXY_CHANNEL}, timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    return True
            except Exception as e:
                print(e)
            cls.change()
            time.sleep(SLEEP_TIME)

    @staticmethod
    def restart_proxy():
        while True:
            try:
                (status, output) = subprocess.getstatusoutput(SERVICE_RESTART_CMD)
                if status == 0:
                    return True
            except Exception as e:
                print(e)
            time.sleep(SLEEP_TIME)


def main():
    while True:
        logger.info('change')
        ADSLProxy.pre_notify()
        time.sleep(SLEEP_TIME)

        ADSLProxy.restart_proxy()
        time.sleep(SLEEP_TIME)

        ADSLProxy.change()
        time.sleep(SLEEP_TIME)

        ADSLProxy.send_and_get_ip()
        time.sleep(INTERVAL)


if __name__ == '__main__':
    logger = logging.getLogger('adsl')  # 设置一个日志器
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    main()
