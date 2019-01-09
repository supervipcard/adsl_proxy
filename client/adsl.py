# -*- coding: utf-8 -*-

import requests
import subprocess
import time
import json
from settings import *


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
            time.sleep(1)

    @classmethod
    def send_and_get_ip(cls):
        while True:
            try:
                response = requests.post(url=VERIFY_URL, data={'token': TOKEN, 'port': PROXY_P0RT, 'channel': PROXY_CHANNEL}, timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    res = json.loads(response.text)
                    print(res)
                    if res['sign']:
                        return True
            except Exception as e:
                print(e)
            time.sleep(1)
            cls.change()

    @classmethod
    def pre_notify(cls):
        while True:
            try:
                response = requests.post(url=NOTIFY_URL, data={'token': TOKEN, 'channel': PROXY_CHANNEL}, timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    return True
            except Exception as e:
                print(e)
            time.sleep(1)
            cls.change()

    @staticmethod
    def restart_proxy():
        while True:
            try:
                (status, output) = subprocess.getstatusoutput(SERVICE_RESTART_CMD)
                if status == 0:
                    return True
            except Exception as e:
                print(e)
            time.sleep(1)


def main():
    while True:
        ADSLProxy.pre_notify()
        time.sleep(1)
        print(1)
        ADSLProxy.restart_proxy()
        time.sleep(1)
        print(2)
        ADSLProxy.change()
        time.sleep(1)
        print(3)
        ADSLProxy.send_and_get_ip()
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()
