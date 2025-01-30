"""Decorator to log function calls."""

import datetime
import json
import logging
import threading
import traceback
from functools import wraps

from django.db.models import QuerySet

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)
_thread_locals = threading.local()


def _get_current_tenant():
    """Get the current tenant."""
    return getattr(_thread_locals, "tenant", "default")


def _safe_repr(val):
    """Return a string representation of the value without evaluating it if is a QuerySet."""
    if isinstance(val, QuerySet):
        return f"<QuerySet: {val.query}>"
    return repr(val)


def log_message_jsonl(log_level, message, **kwargs):
    """Format and log the message in JSONL format."""
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "tenant": _get_current_tenant(),
        "loglevel": log_level,
        "message": message,
        **kwargs,
    }
    logger.info(json.dumps(log_entry))


def log_exception_jsonl(exception):
    """Format and log the message in JSONL format."""
    exception_data = {
        "exception": str(exception),
        "stacktrace": traceback.format_exc(),
    }
    log_message_jsonl("WARNING", "Exception occurred", **exception_data)


def _log_function_jsonl(f_name, f_result, f_args: list = None, f_kwargs: list = None) -> None:
    """Format the log message.

    Args:
        f_name: The name of the function.
        f_result: The result of the function.
        f_args: The arguments of the function.
        f_kwargs: The keyword arguments of the function.
    """
    if f_args is None:
        f_args = []
    if f_kwargs is None:
        f_kwargs = []
    data = {
        "function": f_name,
        "result": f_result,
        "args": f_args,
        "kwargs": f_kwargs,
        "timestamp": datetime.datetime.now().isoformat(),
        "tenant": _get_current_tenant(),
        "loglevel": "INFO",
    }
    message = json.dumps(data)
    logger.info(message)


def log_decorator(f):
    """Decorator to log function calls."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        args_repr = [_safe_repr(a) for a in args]
        kwargs_repr = [f"{k}={_safe_repr(v)}" for k, v in kwargs.items()]
        result_repr = repr(result)
        _log_function_jsonl(f.__name__, f_result=result_repr, f_args=args_repr, f_kwargs=kwargs_repr)
        return result

    return wrapper
