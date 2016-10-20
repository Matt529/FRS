from typing import Callable, Dict, Union, Tuple

from util.templatestring import TemplateLike

import abc
import enum

from concurrent.futures import ProcessPoolExecutor, Future

import requests
import collections

from abc import abstractmethod
from threading import Lock

class HttpMethod(enum.Enum):
    HEAD = 0
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

    def __str__(self):
        return self.name

ResourceResult = collections.namedtuple('ResourceResult', ['url', 'response'])
AsyncResourceCallback = Callable[[ResourceResult, Exception], None]
UrlArgs = Dict[str, str]

class Resource(object):
    def __init__(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, url_args: UrlArgs = None, **kwargs):
        url_args = url_args or {}   # type: UrlArgs

        self.url = resource_url.format(**url_args)
        self.method = method
        self.request_modifiers = kwargs
        self.result = None
        self.done = False

    def make_request(self, forced: bool = False) -> ResourceResult:
        if not self.done or forced:
            self.result = ResourceResult(self.url, requests.request(self.method, self.url, **self.request_modifiers))
            self.done = True

        return self.result


class Requester(metaclass=abc.ABCMeta):

    def __init__(self):
        self._resource_queue = collections.deque()
        self._resource_map = {}                     # type: Dict[str, Resource]

    @staticmethod
    def get(resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, **kwargs) -> ResourceResult:
        return ResourceResult(requests.request(method=method.name, url=resource_url.format(*args), **kwargs))

    def push_last(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, identifier: str = None, **kwargs) -> None:
        identifier = identifier or resource_url
        resource = Resource(resource_url, method, *args, **kwargs)

        self._resource_queue.append(identifier)
        self._resource_map[identifier] = resource

    def push_first(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, identifier: str = None, **kwargs) -> None:
        identifier = identifier or resource_url
        resource = Resource(resource_url, method, *args, **kwargs)

        self._resource_queue.appendleft(identifier)
        self._resource_map[identifier] = resource

    def remove_last(self) -> Resource:
        identifier = self._resource_queue.pop()
        return self._remove(identifier)

    def remove_first(self) -> Resource:
        identifier = self._resource_queue.popleft()
        return self._remove(identifier)

    @abstractmethod
    def retrieve(self, identifier: str, forced: bool = False) -> ResourceResult:
        if identifier in self._resource_map:
            resource = self._resource_map[identifier]

            result = resource.make_request(forced=forced)
            self._resource_queue.remove(identifier)
            return result

        raise KeyError("No resource with identifier: %s" % identifier)

    @abstractmethod
    def retrieve_all(self, forced: bool = False) -> dict:
        results = {}

        while not self.is_empty_queue():
            cur_identifier = self._resource_queue.popleft()
            cur_resource = self._resource_map[cur_identifier]
            results[cur_identifier] = cur_resource.make_request(forced=forced)

        return results

    def is_empty_queue(self):
        return len(self._resource_queue) == 0

    @abstractmethod
    def _remove(self, identifier: str) -> Union[Resource, None]:
        if identifier in self._resource_map:
            resource = self._resource_map[identifier]
            del self._resource_map[identifier]

            return resource
        return None


def _async_make_request(resource: Resource, *args, **kwargs):
    return resource.make_request(*args, **kwargs)


_shared_pool = ProcessPoolExecutor(10)


class AsyncRequester(Requester):

    def __init__(self):
        super().__init__()
        self._work_lock = Lock()
        self._futures = {}      # type: Dict[str, Future]

    @staticmethod
    def get(resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, **kwargs) -> Future:
        return _shared_pool.submit(_async_make_request, Resource(resource_url, method, *args, **kwargs))

    def push_last(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, identifier: str = None, **kwargs) -> None:
        identifier = identifier or resource_url
        resource = Resource(resource_url, method, *args, **kwargs)

        with self._work_lock:
            self._resource_queue.append(identifier)
            self._resource_map[identifier] = resource

    def push_first(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, identifier: str = None, **kwargs) -> None:
        identifier = identifier or resource_url
        resource = Resource(resource_url, method, *args, **kwargs)

        with self._work_lock:
            self._resource_queue.appendleft(identifier)
            self._resource_map[identifier] = resource

    def remove_last(self) -> Resource:
        with self._work_lock:
            identifier = self._resource_queue.pop()
        return self._remove(identifier)

    def remove_first(self) -> Resource:
        with self._work_lock:
            identifier = self._resource_queue.popleft()
        return self._remove(identifier)

    def retrieve(self, identifier: str, forced: bool = False) -> ResourceResult:
        if identifier in self._resource_map:
            with self._work_lock:
                resource = self._resource_map[identifier]

            future = self._futures[identifier] = _shared_pool.submit(_async_make_request, resource, forced)
            future.add_done_callback(self.__future_done(identifier))

            return future

        raise KeyError("No resource with identifier: %s" % identifier)

    def retrieve_all(self, forced: bool = False) -> dict:
        results = {}
        while not self.is_empty_queue():
            with self._work_lock:
                identifier = self._resource_queue.popleft()
                resource = self._resource_map[identifier]
            future = self._futures[identifier] = _shared_pool.submit(_async_make_request, resource, forced)

            future.add_done_callback(self.__future_done(identifier))

            results[identifier] = future

        return results

    def _remove(self, identifier: str) -> Union[Future, None]:
        future = None
        if identifier in self._futures:
            future = self._futures[identifier]
            del self._futures[identifier]

        with self._work_lock:
            if identifier in self._resource_map:
                del self._resource_map[identifier]
            self._resource_queue.remove(identifier)

        return future

    def __future_done(self, identifier: str) -> Callable[[Future], None]:
        def handler(future: Future) -> None:
            if future.done():
                with self._work_lock:
                    self._resource_queue.remove(identifier)
        return handler
