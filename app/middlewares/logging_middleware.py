import json
import logging
import time
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.constants.constants import Constants

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id_header = Constants.REQUEST_ID_HEADER
        request_id = request.headers.get(request_id_header) or str(uuid4())
        request.state.request_id = request_id

        logger.info(
            json.dumps(
                {
                    "type": "api-request",
                    "request_id": request_id,
                    "method": str(request.method).upper(),
                    "url": str(request.url),
                }
            ),
        )

        # Next middleware
        response = await call_next(request)
        response.headers[request_id_header] = request_id

        logger.info(
            json.dumps(
                {
                    "type": "api-response",
                    "request_id": request_id,
                    "code": response.status_code,
                    "time": f"{time.time() - start_time}s",
                }
            ),
        )

        return response
