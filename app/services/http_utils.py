import logging
import time
from typing import Optional

import requests


def request_with_retry(
    session: requests.Session,
    method: str,
    url: str,
    retries: int = 3,
    backoff_factor: float = 1.0,
    logger: Optional[logging.Logger] = None,
    **kwargs,
) -> requests.Response:
    """Perform an HTTP request with retry and exponential backoff."""
    logger = logger or logging.getLogger(__name__)
    for attempt in range(1, retries + 1):
        try:
            resp = session.request(method, url, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            logger.warning(
                "Request failed (attempt %s/%s): %s", attempt, retries, exc
            )
            if attempt == retries:
                logger.error("Request permanently failed: %s", exc)
                raise
            sleep_time = backoff_factor * (2 ** (attempt - 1))
            time.sleep(sleep_time)
    raise RuntimeError("Unreachable retry loop")
