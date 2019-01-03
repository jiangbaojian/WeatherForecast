# -*- coding:utf-8 -*-
#__author__: 'Baojian Jiang'
#__time__:'2018/12/24'
# use for get weather info from Web

from urllib import request
import random
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse
import os, re
import pickle
import zlib

class DownloaderSelf:

    def __init__(self, headers=None, proxy=None, num_retries=2, cache=None, delay=5):
        # self.user_agent = user_agent
        self.proxy = proxy
        self.num_retries = num_retries
        self.cache = cache
        self.throttle = ThrottleSelf(delay)
        self.headers = headers

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # server error, ignore result from cache and redownload
                    result = None
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxy) if self.proxy else None
            # header = {'User-Agent': self.user_agent}
            result = self.download(url, headers=self.headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None):
        print('Downloading:', url)
        request_header = request.Request(url=url, data=data, headers=headers or {})
        opener = request.build_opener()
        if proxy:
            proxy_params = {url, proxy}
            opener.add_handler(request.ProxyHandler(proxy_params))
        try:
            response = opener.open(request_header)
            html = response.read()
            code = response.code
        except Exception as e:
            print('Download error:', str(e))
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    return self.download(url, headers, proxy, num_retries-1, data)
                else:
                    code = None
            elif hasattr(e, 'reason'):
                print('error reason:', e.reason)
                code = None
        return {'html': html, 'code': code}

class DiskCacheSelf:

    def __init__(self, cache_dir='cache', expires=timedelta(days=30), compress=True):
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    def url_to_path(self, url):
        '''create file system for url'''
        components = urlparse(url)
        path = components.path
        if not path:
            path = '/index_none.html'
        elif path.endswith('/'):
            path += 'index_none.html'
        filename = components.netloc + path + components.query
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)

    def __setitem__(self, url, result):
        path = self.url_to_path(url).replace('/', '\\')
        print(path)
        floder = os.path.dirname(path)
        if not os.path.exists(floder):
            os.mkdir(floder)
        data = pickle.dumps((result, datetime.now()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)

    def __getitem__(self, url):
        '''load data from  disk'''
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url + 'has expired')
                return result
        else:
            raise KeyError(url + 'does not exist')

    def has_expired(self, timestamp):
        return str(datetime.now()) > (str(timestamp + self.expires))

class ThrottleSelf:
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        '''delay if  have accessed this domain recently'''
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()