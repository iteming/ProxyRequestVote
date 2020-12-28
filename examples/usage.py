import datetime
import json
import random

import requests
from setting import GET_TIMEOUT, TUPLE_NUM, TEST_ANONYMOUS
from loguru import logger

from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError
from asyncio import TimeoutError
from environs import Env

env = Env()
env.read_env()

EXCEPTIONS = (
    ClientProxyConnectionError,
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError,
    AssertionError,
    requests.exceptions.ReadTimeout,
    requests.exceptions.ProxyError,
    requests.exceptions.ConnectTimeout
)

proxypool_url = 'http://proxy.ngrok.chik.cn/random'
target_url = 'http://km.chik.cn/ip'
tou_piao_url = 'https://swuapp.lhb.ink/release/gzh/tou'

def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()

def get_random_open_id():
    wx_str = "ogrqQ0"
    # wx_end_str = "r7XQ0cuVYsbdx0Fx6bns3g"
    wx_end_str = generate_random_str(22)
    logger.debug(f'get open id = {wx_str + wx_end_str}')
    # return "ogrqQ0r7XQ0cuVYsbdx0Fx6bns3g"
    return wx_str + wx_end_str

def generate_random_str(randomlength=22):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True

def crawl(url, proxy, int_count):
    """
    use proxy to crawl page
    :param url: page url
    :param proxy: proxy, such as 8.8.8.8:8888
    :return: html
    """
    try:
        now_time = datetime.datetime.now().strftime('%H')

        if (int(now_time) >= 1) & (int(now_time) < 7):
            print(f'now_time > 1 and < 7 休息时间 {now_time}')
            return (f'now_time > 1 and < 7 休息时间 {now_time}')

        if int_count >= TUPLE_NUM:
            print(f'投票次数已够 {TUPLE_NUM}')
            return (f'投票次数已够 {TUPLE_NUM}')

        response_text = requests.get(url).text
        print(f'response [no proxy] = {response_text}')

        proxies = {'http': 'http://' + proxy}
        response_text_proxy = requests.get(url, proxies=proxies, timeout=GET_TIMEOUT).text
        print(f'response [use proxy] = {response_text_proxy}')

        if is_json(response_text) & is_json(response_text_proxy):
            text = json.loads(response_text)
            text_proxy = json.loads(response_text_proxy)
            if TEST_ANONYMOUS & (text['origin'] == text_proxy['origin']):
                print(f' 非高匿名ip，越过 {response_text_proxy}')
                return (f'非高匿名ip，越过 {response_text_proxy}')
        else:
            return (f' 有响应非 json ')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        data_search = {
            "openid": get_random_open_id(),
            "act": "tou",
            # "cla_id": "160"
            "cla_id": "53"
        }
        tou_piao_text_proxy = requests.post(tou_piao_url, headers=headers, json=data_search, proxies=proxies, timeout=GET_TIMEOUT).text
        print(f'tou_piao1 [success] = {tou_piao_text_proxy}')
        tou_piao_text_proxy = requests.post(tou_piao_url, headers=headers, json=data_search, proxies=proxies, timeout=GET_TIMEOUT).text
        print(f'tou_piao2 [success] = {tou_piao_text_proxy}')
        tou_piao_text_proxy = requests.post(tou_piao_url, headers=headers, json=data_search, proxies=proxies, timeout=GET_TIMEOUT).text
        print(f'tou_piao3 [success] = {tou_piao_text_proxy}')
        int_count = int_count + 3


        text_proxy = json.loads(response_text_proxy)
        real_ip = text_proxy['origin']
        logger.debug(f'tou_piao [success] = {tou_piao_text_proxy} | realIp = {real_ip} | proxy = {proxies} | tuple_num = {int_count}')

        return int_count
    except EXCEPTIONS:
        # logger.error(f'request by proxy {proxy.string()} from {url} error [{exc}]')
        print(f'timeout ***** ')
        return "timeout"

def main(int_count):
    """
    main method, entry point
    :return: none
    """
    proxy = get_random_proxy()
    print('get random proxy', proxy)
    return_int_count = crawl(target_url, proxy, int_count)
    if isinstance(return_int_count, int):
        print("return_int_count is int")
        return return_int_count
    return int_count


if __name__ == '__main__':
    main()
