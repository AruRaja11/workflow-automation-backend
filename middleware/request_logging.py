import logging
import time 
import uuid

from fastapi import Request

from core.logging_cofig import request_id_context


logger = logging.getLogger(__name__)


async def request_logging_middleware(request:Request, call_next):

    request_id = str(uuid.uuid4())
    context_token = request_id_context.set(request_id)
    start_time = time.perf_counter()

    logger.info(
        "Request started: %s %s",
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)
    except Exception as e:
        duration = time.perf_counter() - start_time
        logger.error(
            "Request failed: %s %s exception_type=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            type(e).__name__,
            duration * 1000,
        )

        raise
    else:
        duration = time.perf_counter() - start_time

        logger.info(
            "Request completed: %s %s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duration * 1000,
        )

        response.headers["X-Request-ID"] = request_id
        return response


    finally:
        request_id_context.reset(context_token)
