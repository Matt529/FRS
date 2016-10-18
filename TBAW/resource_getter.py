from typing import Callable, Optional

from util.templatestring import TemplateLike

import abc
import enum

from concurrent.futures import ProcessPoolExecutor

import requests
import collections


class HttpMethod(enum.Enum):
    HEAD = 0
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

    def __str__(self):
        return self.name

ResourceResult = collections.namedtuple('ResourceResult', ['response'])
AsyncResourceCallback = Callable[[ResourceResult, Exception], None]


class Resource(object):
    def __init__(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, **kwargs):
        self.url = resource_url.format(*args)
        self.method = method
        self.request_modifiers = kwargs

    def make_request(self) -> ResourceResult:
        return ResourceResult(requests.request(self.method, self.url, **self.request_modifiers))


class ResourceGetter(metaclass=abc.ABCMeta):

    def __init__(self):
        self._resource_queue = collections.deque()   # type:

    @staticmethod
    def get(resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, **kwargs) -> ResourceResult:
        return ResourceResult(requests.request(method=method.name, url=resource_url.format(*args), **kwargs))

    def push_last(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, **kwargs) -> None:
        self._resource_queue.append(Resource(resource_url, method, *args, **kwargs))

    def push_first(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, **kwargs) -> None:
        self._resource_queue.appendleft(Resource(resource_url, method, *args, **kwargs))

    def remove_last(self) -> Resource:
        return self._resource_queue.pop()

    def remove_first(self) -> Resource:
        return self._resource_queue.popleft()

    def next(self) -> ResourceResult:
        return self.remove_first().make_request()


class AsyncResourceGetter(ResourceGetter):

    def __init__(self, max_concurrency: int = 10):
        self._concurrency = max_concurrency

