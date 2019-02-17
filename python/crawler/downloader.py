# -*- coding: utf-8 -*-

"""
Provide download function by request
"""

from datetime import datetime
import logging
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup


class Throttle(object):
    """Throttle downloading by sleeping between requests to same domain."""
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urllib.parse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()


class Downloader(object):
    """Convenient download of web pages or caller to call api.

    Args:
        delay: Interval between downloads (seconds)
        num_retries: Number of retries when downloading errors
        timeout: Download timeout
    """
    def __init__(self, delay=5, user_agent='awsl', proxies=None, num_retries=1,
                 timeout=60, cache=None, auth=None):
        self.session = requests.Session()
        self.session.headers.update({'user-agent': user_agent})
        self.session.proxies = proxies
        self.session.auth = auth
        self.throttle = Throttle(delay)
        self.num_retries = num_retries
        self.timeout = timeout
        self.cache = cache

    def get_from_cache(self, request):
        """Try to get the result of the request from the cache."""
        result = None
        if self.cache:
            result = self.cache.get(request.url)
            if result and self.num_retries > 0 and 500 <= result['code'] < 600:
                result = None
        return result

    def prepare_request(self, url, params=None):
        """Build requests based on the provided url and parameters."""
        request = requests.Request('GET', url, params=params)
        return self.session.prepare_request(request)

    def send_request(self, request, num_retries):
        """Send request and return response object."""
        self.throttle.wait(request.url)
        try:
            logging.info('Downloading: %s' % request.url)
            response = self.session.send(request, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.warn('Download error: %s' % e)
            if num_retries > 0 and 500 <= response.status_code < 600:
                return self.send_request(request, num_retries - 1)
        except requests.exceptions.RequestException:
            logging.error('Download faild: %s' % request.url)
            response = None
        return response

    def text(self, url, params=None, encoding=None):
        """Download web content in text format or html."""
        request = self.prepare_request(url, params)
        result = self.get_from_cache(request)
        if result is None:
            response = self.send_request(request, self.num_retries)
            if response:
                if encoding:
                    response.encoding = encoding
                result = {'text': response.text, 'code': response.status_code}
                if self.cache:
                    self.cache[request.url] = result
        return result['text']

    def json(self, url, params=None):
        """Access the api and return the json object."""
        request = self.prepare_request(url, params)
        result = self.get_from_cache(request)
        if result is None:
            response = self.send_request(request, self.num_retries)
            if response:
                result = {'json': response.json(), 'code': response.status_code}
                if self.cache:
                    self.cache[request.url] = result
        return result['json']
