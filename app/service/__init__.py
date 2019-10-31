import asyncio
import inspect
import json
import time
from collections import OrderedDict
import ssl

import aiohttp
from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web import Request, Response
from aiohttp.web_urldispatcher import UrlDispatcher

from app.service.connection import service_connection
from app.service.exceptions import APIServiceException

__version__ = '0.1.0'

DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


class RestEndpoint:
    def __init__(self):
        self.methods = {}

        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name, method):
        self.methods[method_name.upper()] = method

    async def dispatch(self, method, url, **kwargs):
        method = self.methods.get(method.upper())
        if not method:
            raise HTTPMethodNotAllowed('', DEFAULT_METHODS)

        return await method(url, **kwargs)


class MixinEndpoint(RestEndpoint):
    def __init__(self, session):
        super().__init__()
        self.session = session

    async def get(self, url, **kwargs):
        async with self.session.get(url, ssl=ssl.SSLContext()) as response:
            return await response.json()

    async def post(self, url, **kwargs):
        async with self.session.get(url, ssl=ssl.SSLContext()) as response:
            return await response.json()


class AsyncRequest:
    def __init__(self, urls: list):
        self.urls = urls
        pass

    def run(self):
        return asyncio.run(self.fetch_all())

    async def fetch_all(self, **kwargs):
        # Asynchronous context manager.  Prefer this rather
        # than using a different session for each GET request
        async with aiohttp.ClientSession() as session:
            endpoint = MixinEndpoint(session)
            results = await asyncio.gather(*[endpoint.get(url, **kwargs) for url in self.urls], return_exceptions=True)
            return results