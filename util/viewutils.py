from functools import wraps
from typing import List, Mapping, Union, Any

from django.http import QueryDict, HttpResponseNotAllowed
from django.utils.decorators import available_attrs

from util.templatestring import TemplateString

def make_querydict_from_request(func):
    @wraps(func, assigned=available_attrs(func))
    def inner(request, *args, **kwargs):
        if request.method not in ['GET', 'POST']:
            read_request_body_to(request, request.method)
        return func(request, *args, **kwargs)
    return inner


def require_http_methods_plus(method_types: List[str], required_args: Union[Mapping[str, List[str]], List[str]]=None,
                              method_props: Mapping[str, List[str]]=None):
    """
    Enhances the possible functionality of the standard require_http_methods function from django.

    If just method_types is provided then this decorator acts exactly the same way as the standard function.

    If required_args is provided as a list then whatever method type is provided, the view arguments are verified to
    ensure all arguments in required_args appear as a key in the view arguments.

    If required_args is provided as a dictionary, then if the method type appears in that dictionary as a key it must
    be mapped to a list of argument names. This list of argument names is then verified the same way as above.

    If method_props is provided it must be a dictionary. If the method_type appears in that dictionary then it must
    be mapped to a list of property names. This list of property names is then checked against the properties in the
    QueryDict for our request method. If any property is missing, an error occurs.

    :param method_types: List of Request Method names allowed to pass through
    :param required_args: List of requires arguments for any request method or Map from Request Method names to required
                        arguments
    :param method_props: Map from Request Method names to required method properties
    """

    if required_args is None:
        required_args = {}
    if method_props is None:
        method_props = {}

    invalid_type = TemplateString("{method} is not one of the allowed request methods ({types})!")
    missing_props = TemplateString("Request of type {method} must have following properties: {props}")
    missing_args = TemplateString("Request missing arguments. Has {args}, missing {missing}")

    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):

            # Verify method is at least a valid method type
            if request.method not in method_types:
                print("METHOD NOT ALLOWED", invalid_type(method=request.method, types=method_types))
                return HttpResponseNotAllowed(method_types)

            # Check that all required properties are in QueryDict, if any are required
            method_dict = getattr(request, request.method)
            if request.method in method_props and len([x for x in method_props[request.method] if x not in method_dict]) > 0:
                print("METHOD NOT ALLOWED", missing_props(method=request.method, props=method_props))
                return HttpResponseNotAllowed(
                    method_types,
                    reason=missing_props(method=request.method, props=method_props)
                )

            # Sanitize, either required_args is a list or map, normalize to a list
            required_args_list = required_args
            if isinstance(required_args, dict):
                required_args_list = required_args[request.method] if request.method in required_args else []

            # Check that all required arguments exist in the view arguments
            missing_args_list = [x for x in required_args_list if x not in kwargs]
            if len(missing_args_list) > 0:
                print("METHOD NOT ALLOWED", missing_args(required_args_list-missing_args_list, missing_args_list))
                return HttpResponseNotAllowed(
                    method_types,
                    reason=missing_args(args=(required_args_list-missing_args_list), missing=missing_args_list)
                )

            return func(request, *args, **kwargs)

        return inner

    return decorator


def ajax_success(**kwargs) -> dict:
    kwargs.update({'success': True})
    return kwargs


def ajax_failure(**kwargs) -> dict:
    kwargs.update({'success': False})
    return kwargs


def is_safe_request(method: str) -> bool:
    while hasattr(method, 'method'):
        method = method.method
    return method in ('GET', 'HEAD')


def read_request_body_to_post(request) -> None:
    """
    Takes a request and stores the request body into a POST QueryDict. By default only the GET QueryDict exists.

    :param request: Request object
    """
    request.POST = QueryDict(request.body)


def read_request_body_to(request, method: str='POST') -> None:
    """
    Takes a request method (or really any string) and a request object and stores the request body into a QueryDict
    which is then stored in the request at a property named after the method provided.

    read_request_body_to(req) -> req.POST now exists
    read_request_body_to(req, "HEAD") -> req.HEAD now exists
    read_request_body_to(req, "delete") -> req.DELETE now exists

    :param request:
    :param method:
    :return:
    """
    setattr(request, method.upper(), QueryDict(request.body))

