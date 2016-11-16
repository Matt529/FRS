from typing import Callable, Dict, Union, List, Tuple

from util.templatestring import TemplateLike

import uuid
import enum

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, Future

import requests
import collections

from abc import abstractmethod
from threading import RLock


class HttpMethod(enum.Enum):
    """
    Available HTTP Methods
    """
    HEAD = 0
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

    def __str__(self):
        return self.name


class ResourceResult(object):
    """
    Wrapping class for the results of an HTTP request made using requests.
    """

    def __init__(self, url: str, response: requests.Response):
        self.url = url
        self.response = response

    def __str__(self):
        return '%s[%s]' % (type(self).__name__, self.url)


AsyncResourceCallback = Callable[[ResourceResult, Exception], None]
UrlArgs = Dict[str, str]


class Resource(object):
    """
    Representation for a desired Resource at a specified URL.
    """

    def __init__(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, url_args: UrlArgs = None, **kwargs):
        """
        :param resource_url:
            URL as a string or as a TemplateString. The TemplateString is immediately formatted using the given UrlArgs
        :param method:
            HTTP Method
        :param args:
            Positional arguments for url template
        :param url_args:
            Dictionary of keyword arguments for url template
        :param kwargs:
            Keyword arguments to pass to requests.request when request is made
        """
        url_args = url_args or {}   # type: UrlArgs

        self.url = resource_url.format(*args, **url_args)
        self.method = method
        self.request_modifiers = kwargs
        self.result = None
        self.done = False

    def make_request(self, forced: bool = False) -> ResourceResult:
        if not self.done or forced:
            self.result = ResourceResult(self.url, requests.request(self.method.name, self.url, **self.request_modifiers))
            self.done = True

        return self.result

# struct-like data container for all that is needed to represent a Resource
# Convenient as a parameter
_ResourceDescriptor = collections.namedtuple('_ResourceDescriptor', ['identifier', 'url', 'method', 'args', 'kwargs'])


def make_resource_descriptor(url: str, method: HttpMethod, *args, identifier: str = None, **kwargs):
    """
    Utility function for creating _ResourceDescriptor objects, this is the intended way of creating them.

    :param url:
        Resource URL
    :param method:
        HTTP Method for Resource
    :param args:
        Positional Arguments for Resource, these are used to format Resource URL if needed, not required
    :param identifier:
        Identifier for Resource, can be none. If none, a unique identifier will be generated
    :param kwargs:
        Keyword Arguments for Resource, these are used to format Resource URL if needed, not required
    :return:
        _ResourceDescriptor wrapper for parameters
    """
    return _ResourceDescriptor(identifier, url, method, args, kwargs)


def _make_default_identifier(url: TemplateLike, method: HttpMethod) -> str:
    """
    Creates a string identifier for a resource from the url and method name and a random UUID generated using uuid4

    :param url:
        Resource URL
    :param method:
        HTTP Method for Resource
    :return:
        String identifier for resource
    """
    return "%s:%s:%s" % (url, method.name, uuid.uuid4())


class Requester(object):
    """
    Queues resources and handles resource retrieval using the requests API.

    The retrievals in this case are done synchronously, thus any options using this requester are likely to
    be IO-bounded.
    """

    def __init__(self):
        self._resource_queue = collections.deque()
        self._resource_map = {}                     # type: Dict[str, Resource]

    @staticmethod
    def get(resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, url_args: UrlArgs,  **kwargs) -> ResourceResult:
        """
        Immediately retrieve a resource from the given resource URL using the given HTTP method

        :param resource_url:
            Resource URL
        :param method:
            HTTP Method
        :param args:
            Positional arguments for formatting URL if needed
        :param url_args:
            Dictionary of keyword arguments for formatting URL if needed
        :param kwargs:
            Keyword arguments to pass to requests.request
        :return:
            ResourceResult for resource at the given URL
        """
        return ResourceResult(resource_url, requests.request(method=method.name, url=resource_url.format(*args, **url_args), **kwargs))

    def push_all_last(self, res: _ResourceDescriptor, *args: List[_ResourceDescriptor]):
        """
        Pushes resource in bulk onto resource queue from the back. The last Resource Descriptor provided will be the
        last resource in the resource queue. If any identifiers are not provided, they will be generated and stored back into
        the Resource Descriptor.

        :param res:
            First resource descriptor
        :param args:
            All other resource descriptors
        """

        args = [res, *args]     # type: List[_ResourceDescriptor]

        if not all([isinstance(x, _ResourceDescriptor) for x in args]):
            raise TypeError('All arguments must be a Resource Descriptor')

        for res in args:
            res.identifier = self.push_last(res.url, res.method, *res.args, identifier=res.identifier, **res.kwargs)

    def push_all_first(self, res: _ResourceDescriptor, *args: List[_ResourceDescriptor]) -> List[TemplateLike]:
        """
        Pushes resource in bulk onto resource queue from the front. The last Resource Descriptor provided will be the
        first resource in the resource queue. If any identifiers are not provided, they will be generated and stored back into
        the Resource Descriptor.

        :param res:
            First resource descriptor
        :param args:
            All other resource descriptors
        """

        args = [res, *args]     # type: List[_ResourceDescriptor]

        if not all([isinstance(x, _ResourceDescriptor) for x in args]):
            raise TypeError('All arguments must be a Resource Descriptor')

        for res in args:
            res.identifier = self.push_first(res.url, res.method, *res.args, identifier=res.identifier, **res.kwargs)

        return [x.identifier for x in args]

    def push_last(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, identifier: str = None, **kwargs) -> TemplateLike:
        """
        Pushes a new Resource onto the back of the resource queue.

        :param resource_url:
            Resource URL
        :param method:
            HTTP Method
        :param args:
            Positional args for formatting Resource URL
        :param identifier:
            Resource identifier, can be none. If none, a unique identifier is generated
        :param kwargs:
            Keyword arguments to pass to Resource, url_args, if povidied, should be a dict of keyword formatting
            arguments, all other keyword arguments are passed to requests.request
        :return:
            Resource Identifier String
        """

        identifier = identifier or _make_default_identifier(resource_url, method)
        resource = Resource(resource_url, method, *args, **kwargs)

        self._resource_queue.append(identifier)
        self._resource_map[identifier] = resource
        return identifier

    def push_first(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, identifier: str = None, **kwargs) -> TemplateLike:
        """
        Pushes a new Resource onto the front of the resource queue.

        :param resource_url:
            Resource URL
        :param method:
            HTTP Method
        :param args:
            Positional args for formatting Resource URL
        :param identifier:
            Resource identifier, can be none. If none, a unique identifier is generated
        :param kwargs:
            Keyword arguments to pass to Resource, url_args, if povidied, should be a dict of keyword formatting
            arguments, all other keyword arguments are passed to requests.request
        :return:
            Resource Identifier String
        """

        identifier = identifier or _make_default_identifier(resource_url, method)
        resource = Resource(resource_url, method, *args, **kwargs)

        self._resource_queue.appendleft(identifier)
        self._resource_map[identifier] = resource
        return identifier

    def remove_last(self) -> TemplateLike:
        """
        Removes the most recently added Resource from the resource queue.

        :return:
            Identifier of the resource that was removed
        :except IndexError:
            If Resource Queue is empty
        """

        if self.is_empty_queue():
            raise IndexError('No requests are currently queued!')

        identifier = self._resource_queue.pop()
        return self._remove(identifier)

    def remove_first(self) -> TemplateLike:
        """
        Removes the least recently added Resource from the resource queue.

        :return:
            Identifier of the resource that was removed
        :except IndexError:
            If Resource Queue is empty
        """

        if self.is_empty_queue():
            raise IndexError('No requests are currently queued!')

        identifier = self._resource_queue.popleft()
        return self._remove(identifier)

    @abstractmethod
    def retrieve(self, identifier: str, forced: bool = False) -> ResourceResult:
        """
        Retrieve the next Resource in the resource queue.

        :param identifier:
            Identifier of the resource to retrieve
        :param forced:
            If the resource is already retrieved, it's result is cached. Setting forced to true means the request is
            made again and the new result will be cached.
        :return:
            ResourceResult for the request response
        :except KeyError:
            Identifier is not in resource map
        """

        if identifier in self._resource_map:
            resource = self._resource_map[identifier]

            result = resource.make_request(forced=forced)
            return result

        raise KeyError("No resource with identifier: %s" % identifier)

    @abstractmethod
    def retrieve_all(self, forced: bool = False) -> Dict[str, ResourceResult]:
        """
        Retrieve all remaining resource in resource queue. This action will clear the resource map and resource queue,
        essentially acting like a reset call.

        :param forced:
            If a resource has already been retrieved, it's result is cached. Setting forced to true means the request is
            made again and the new result will be cached.
        :return:
            ResourceResult for the request response
        :except KeyError:
            Identifier is not in resource map
        """
        results = {}

        while not self.is_empty_queue():
            cur_identifier = self._resource_queue.popleft()
            cur_resource = self._resource_map[cur_identifier]
            results[cur_identifier] = cur_resource.make_request(forced=forced)
            del self._resource_map[cur_identifier]

        return results

    @abstractmethod
    def reset(self):
        self._resource_queue.clear()
        self._resource_map.clear()

    def size(self):
        """
        :return:
            Number of resources left in resource queue
        """
        return len(self._resource_queue)

    def is_empty_queue(self):
        """
        :return:
            True if size of resource queue is 0, false otherwise
        """
        return len(self._resource_queue) == 0

    @abstractmethod
    def _remove(self, identifier: str) -> TemplateLike:
        """
        Removes identifier from resource map if the identifier is a key in the map.

        :param identifier:
            Identifier of resource to remove
        :return:
            Identifier that was removed
        :except KeyError:
            Identifier is not a key in the resource map
        """
        if identifier in self._resource_map:
            del self._resource_map[identifier]
            return identifier
        raise KeyError("No resource with identifier: %s" % identifier)

    def __len__(self):
        return self.size()


# Helper method, since a method cannot be used as a ProcessPool submission, this function is used which then calls
# the resource that is serialized and then passed.
def _async_make_request(resource: Resource, *args, **kwargs):
    return resource.make_request(*args, **kwargs)

#
#   The default for AsyncRequester is currently to use a ThreadPool. Threads in python suffer from GIL (Global
#   Interpreter Lock) and, similar to Node.js, the Threads never run truly Asynchronously, but are instead interleaved,
#   this still provides meaningful benefits for IO but will be much more bounded than using a ProcessPool, which makes
#   ensuring IPC works a bit more complicated (serializing a requests.Response object may either just work or require
#   some painful monkey patching...).
#
#   So if the ThreadPool ends up being insufficient for our purposes, making the default use the shared ProcessPool
#   may be more beneficial and has a guaranteed speed up (by avoiding GIL and being truly async) *if* it works.
#
#   If we decide to use processes in the future, see: https://github.com/ross/requests-futures
#

# shared process pool to ensure we never exceed 10 processes
_shared_pool = ProcessPoolExecutor(10)


class AsyncRequester(Requester):
    """
    Queues resources and handles resource retrieval using the requests API.

    The retrievals in this case are done asynchronously using processes (and not threads) to avoid Global Interpreter
    Lock. When initializing a ThreadPool is used by default. This means the benefits may be reduced by Global
    Interpreter Lock. If use_threads is set to false then a global shared process pool (of 10 processes) are used. By
    being separate processes, they avoid Global Interpreter Lock but IPC requires any data that needs to be
    communicated to be picklable (serializable).
    """

    def __init__(self, use_threads: bool = True):
        """
        :param use_threads:
            If true, use personal ThreadPool, otherwise use global shared process pool (see class docs for details)
        """
        super().__init__()

        # Reentrant Lock to ensure no spawned threads screw up queue/map/future-map state
        self._work_lock = RLock()
        self._pool = ThreadPoolExecutor(10) if use_threads else _shared_pool
        # Cached futures
        self._futures = {}      # type: Dict[str, Future]

    @staticmethod
    def get(resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, **kwargs) -> Future:
        return _shared_pool.submit(_async_make_request, Resource(resource_url, method, *args, **kwargs))

    def request(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, **kwargs) -> Future:
        return self._pool.submit(_async_make_request, Resource(resource_url, method, *args, **kwargs))

    def push_last(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, identifier: str = None, **kwargs) -> TemplateLike:
        """
        Pushes a new Resource onto the back of the resource queue.

        :param resource_url:
            Resource URL
        :param method:
            HTTP Method
        :param args:
            Positional args for formatting Resource URL
        :param identifier:
            Resource identifier, can be none. If none, a unique identifier is generated
        :param kwargs:
            Keyword arguments to pass to Resource, url_args, if povidied, should be a dict of keyword formatting
            arguments, all other keyword arguments are passed to requests.request
        :return:
            Resource Identifier String
        """

        identifier = identifier or _make_default_identifier(resource_url, method)
        resource = Resource(resource_url, method, *args, **kwargs)

        with self._work_lock:
            self._resource_queue.append(identifier)
            self._resource_map[identifier] = resource

        return identifier

    def push_first(self, resource_url: TemplateLike, method: HttpMethod = HttpMethod.GET, *args, identifier: str = None, **kwargs) -> TemplateLike:
        """
        Pushes a new Resource onto the front of the resource queue.

        :param resource_url:
            Resource URL
        :param method:
            HTTP Method
        :param args:
            Positional args for formatting Resource URL
        :param identifier:
            Resource identifier, can be none. If none, a unique identifier is generated
        :param kwargs:
            Keyword arguments to pass to Resource, url_args, if povidied, should be a dict of keyword formatting
            arguments, all other keyword arguments are passed to requests.request
        :return:
            Resource Identifier String
        """

        identifier = identifier or _make_default_identifier(resource_url, method)
        resource = Resource(resource_url, method, *args, **kwargs)

        with self._work_lock:
            self._resource_queue.appendleft(identifier)
            self._resource_map[identifier] = resource

        return identifier

    def remove_last(self) -> TemplateLike:
        """
        Removes the most recently added Resource from the resource queue.

        :return:
            Identifier of the resource that was removed
        :except IndexError:
            If Resource Queue is empty
        """

        with self._work_lock:
            identifier = self._resource_queue.pop()
        return self._remove(identifier)

    def remove_first(self) -> TemplateLike:
        """
        Removes the least recently added Resource from the resource queue.

        :return:
            Identifier of the resource that was removed
        :except IndexError:
            If Resource Queue is empty
        """

        with self._work_lock:
            identifier = self._resource_queue.popleft()
        return self._remove(identifier)

    def retrieve(self, identifier: str, forced: bool = False) -> Future:
        """
        Retrieve the next Resource in the resource queue.

        :param identifier:
            Identifier of the resource to retrieve
        :param forced:
            If the resource is already retrieved, it's result is cached. Setting forced to true means the request is
            made again and the new result will be cached.
        :return:
            Future for the given resource. A promise of data in the future, can be used to wait for results... or errors
            later.
        :except KeyError:
            Identifier is not in resource map
        """

        with self._work_lock:
            # If a future is already cached then we should return that future
            # If forced is true, then the cached future is cancelled if not yet complete, either way it's entry is then
            # overwritten.
            if identifier in self._futures:
                if not forced:
                    return self._futures[identifier]
                elif not (self._futures[identifier].done() or self._futures[identifier].cancelled()):
                    self._futures[identifier].cancel()

        if identifier in self._resource_map:
            with self._work_lock:
                resource = self._resource_map[identifier]
                future = self._futures[identifier] = self._pool.submit(_async_make_request, resource, forced)

            requester_callback = self.__future_done(identifier)
            future.add_done_callback(requester_callback)
            self.__monkey_patch_future(future, requester_callback)

            return future

        raise KeyError("No resource with identifier: %s" % identifier)

    def retrieve_all(self, forced: bool = False) -> Dict[str, Future]:
        """
        Retrieve all remaining resource in resource queue. This action will clear the resource map and resource queue,
        essentially acting like a reset call. All of the results are returned initially as Futures, promises of future
        data that can be used to wait for exceptions or reuslts in the future.

        :param forced:
            If a resource has already been retrieved, it's result is cached. Setting forced to true means the request is
            made again and the new result will be cached.
        :return:
            Futures of all remaining Resources in resource queue
        :except KeyError:
            Identifier is not in resource map
        """

        results = {}
        with self._work_lock:
            while not self.is_empty_queue():
                identifier = self._resource_queue.popleft()
                results[identifier] = self.retrieve(identifier)

        return results

    def reset(self):
        with self._work_lock:
            super().reset()

            for future in self._futures.values():
                if not future.done():
                    future.cancel()

            self._futures.clear()

    def _remove(self, identifier: str) -> TemplateLike:
        if identifier in self._futures:
            del self._futures[identifier]

        with self._work_lock:
            if identifier in self._resource_map:
                del self._resource_map[identifier]
            else:
                raise KeyError("No resource with identifier: %s" % identifier)

        return identifier

    def __monkey_patch_future(self, future: Future, requester_cb) -> Future:
        from types import MethodType
        from concurrent.futures._base import CANCELLED, CANCELLED_AND_NOTIFIED, FINISHED

        def _special_add_done_callback(self, fn):
            with self._condition:
                if self._state not in [CANCELLED, CANCELLED_AND_NOTIFIED, FINISHED]:
                    if len(self._done_callbacks) == 0:
                        self._done_callbacks = [fn, requester_cb]
                    else:
                        self._done_callbacks = self._done_callbacks[:-1] + [fn, requester_cb]
                    return
            fn(self)

        future.add_done_callback = MethodType(_special_add_done_callback, future)

    def __future_done(self, identifier: str) -> Callable[[Future], None]:
        def handler(future: Future) -> None:
            if future.done():
                self._remove(identifier)
        return handler
