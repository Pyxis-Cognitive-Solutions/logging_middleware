# logging_middleware

A simple Django middleware for logging requests, function calls, and exceptions.

## Installation

You can install `logging_middleware` using pip:

```sh
pip install git+https://github.com/Pyxis-Cognitive-Solutions/logging_middleware
```

## Usage

1. Add `logging_middleware.JsonLoggingMiddleware` to the `MIDDLEWARE` list in your Django settings:

```python
MIDDLEWARE = [
    ...
    'logging_middleware.JsonLoggingMiddleware',
    ...
]
```

## Features

- Logs incoming requests, including method, URL, and headers.
- Logs function calls with arguments and return values.
- Logs exceptions with stack traces for easier debugging.

## License

This project is licensed under the MIT License.
