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
    """
    Rest Endpoints Abstract Class used to dispatch asynchronous requests. Raise Errors if any of the default method
     is not defined in the subclass . Also raises error if any method not listed in default is called in dispatch

    """

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
    """
    Subclasses the RestEndpoint and implement async  get and post method
    :arg: session
    :type session: aiohttp.ClientSession
    """

    def __init__(self, session: aiohttp.ClientSession):
        super().__init__()
        self.session = session

    async def get(self, url, **kwargs):
        async with self.session.get(url, ssl=ssl.SSLContext()) as response:
            return await response.json()

    async def post(self, url, **kwargs):
        async with self.session.get(url, ssl=ssl.SSLContext()) as response:
            return await response.json()


class AsyncRequest:
    """Gets the lists of the urls and fetch them asynchronously
    :arg urls: list of the urls to be iterated and run asynchronously
    :type urls: iterable
    """

    def __init__(self, urls: iter):
        self.urls = urls
        pass

    def run(self):
        """
        Called to run the fetch the the requests of the urls asynchronously
        :return: list of urls responses in the order of url definition
        """
        return asyncio.run(self.fetch_all())

    async def fetch_all(self, **kwargs):
        # Asynchronous context manager.  Prefer this rather
        # than using a different session for each GET request
        async with aiohttp.ClientSession() as session:
            endpoint = MixinEndpoint(session)
            results = await asyncio.gather(*[endpoint.get(url, **kwargs) for url in self.urls], return_exceptions=True)
            return results
