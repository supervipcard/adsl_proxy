# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import requests
import redis
import time
import logging
import logging.handlers
from settings import *


class VerifyHandler(tornado.web.RequestHandler):
    def post(self):
        token = self.get_body_argument('token', default=None, strip=False)
        port = self.get_body_argument('port', default=None, strip=False)
        channel = self.get_body_argument('channel', default=None, strip=False)

        try:
            if token == TOKEN and port:
                ip = self.request.remote_ip
                proxy = ip + ':' + port

                redis_client = redis.Redis(connection_pool=redis_pool)

                # 检测IP是否在黑名单中
                # if redis_client.sismember(IP_BLACKLIST_KEY, proxy) == 0:
                result = self.test_proxy(proxy)
                if result:
                    redis_client.set(channel, proxy)
                    logger.info('{channel} {proxy} is available'.format(channel=channel, proxy=proxy))
                    self.write({'sign': True, 'proxy': proxy, 'msg': 'success'})
                else:
                    logger.warning('{channel} {proxy} is bad'.format(channel=channel, proxy=proxy))
                    self.write({'sign': False, 'proxy': proxy, 'msg': 'Wrong Proxy'})
                # else:
                #     logger.warning('{channel} {proxy} in blacklist'.format(channel=channel, proxy=proxy))
                #     self.write({'sign': False, 'proxy': proxy, 'msg': 'Wrong Proxy'})
            else:
                logger.warning('无效的请求')
                self.send_error(400)
        except:
            logger.error('服务异常')
            self.send_error(500)

    @staticmethod
    def test_proxy(proxy):
        try:
            response = requests.get(url=TEST_URL, proxies={'http': proxy, 'https': proxy}, timeout=DOWNLOAD_TIMEOUT)
            if response.status_code == 200:
                return True
        except:
            logging.exception('connect error')


class NotifyHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(10)

    @tornado.gen.coroutine
    def post(self):
        token = self.get_body_argument('token', default=None, strip=False)
        channel = self.get_body_argument('channel', default=None, strip=False)

        try:
            if token == TOKEN:
                yield self.extra(channel)
                logger.info('通道{channel} 即将收到新代理'.format(channel=channel))
                self.finish()
            else:
                logger.warning('无效的请求')
                self.send_error(400)
        except:
            logger.error('服务异常')
            self.send_error(500)

    @run_on_executor
    def extra(self, channel):
        redis_client = redis.Redis(connection_pool=redis_pool)
        if not ISSINGLE:
            while True:
                keys = redis_client.keys('%s*' % REDIS_PROXY_KEY)
                if len(keys) == 1 and keys[0].decode('utf-8') == channel:    # 如果只有该通道存在，暂时不删除
                    logger.info('通道{channel} 等待3秒'.format(channel=channel))
                    time.sleep(3)
                else:
                    break
        redis_client.delete(channel)


def make_app():
    return tornado.web.Application([
        (r"/verify", VerifyHandler),
        (r"/notify", NotifyHandler)
    ])


if __name__ == '__main__':
    # assert REDIS_PROXY_KEY not in IP_BLACKLIST_KEY, 'IP_BLACKLIST_KEY name can not contain REDIS_PROXY_KEY name'

    logger = logging.getLogger('service')  # 设置一个日志器
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

    fileHandler = logging.handlers.TimedRotatingFileHandler(filename="log_file", when='D', interval=1, backupCount=5, encoding='utf-8')
    fileHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)

    redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, max_connections=POOL_SIZE)

    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
