import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi.requests import Request
from fastapi.responses import Response
from utils.logger.logger import Logger


class TimingStats(object):
    def __init__(self, name=None):
        self.name = name
        self.start_time = None
        self.start_cpu_time = None
        self.end_time = None
        self.end_cpu_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def __enter__(self):
        self.start()
        return self

    @property
    def time(self):
        return self.end_time - self.start_time

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()


class AccessLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, log_name):
        super().__init__(app)
        self.log_name = log_name
        self.logger = Logger().get_logger(log_name=log_name)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = None
        with TimingStats("context") as stats:
            response = await call_next(request)

            # write log to

        logger = logging.LoggerAdapter(self.logger, dict(
            request_id=request.state.request_id,
            time_cost=stats.time,
            request_method=request.method,
            request_path=request.scope["path"],
            response_code=response.status_code
        ))
        logger.info("")

        response.headers["x-request-id"] = request.state.request_id
        return response


class RequestIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, mode="uuid"):
        super().__init__(app)
        self.mode = mode

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        with RequestIdContext() as request_id:
            request.state.request_id = request_id
            return await call_next(request)


class RequestIdContext(object):

    def __init__(self, mode="uuid"):
        self.mode = mode

    def __enter__(self):
        if self.mode == "uuid":
            return generate_request_id_by_uuid()
        else:
            return ""

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def generate_request_id_by_uuid():
    """
    generate uuid for request id
    :return:
    """
    return str(uuid.uuid4())
