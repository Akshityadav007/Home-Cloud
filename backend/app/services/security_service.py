from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
import subprocess
from pathlib import Path

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):

    _requests = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if settings.RATE_LIMIT_REQUESTS <= 0:
            return await call_next(request)

        client = request.client.host if request.client else "unknown"
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(
            seconds=settings.RATE_LIMIT_WINDOW_SECONDS
        )
        requests = self._requests[client]

        while requests and requests[0] < window_start:
            requests.popleft()

        if len(requests) >= settings.RATE_LIMIT_REQUESTS:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )

        requests.append(now)
        return await call_next(request)


class MalwareScanner:

    @staticmethod
    def scan_or_raise(path: str, original_filename: str):
        extension = Path(original_filename).suffix.lower()
        blocked = {
            item.strip().lower()
            for item in settings.BLOCKED_UPLOAD_EXTENSIONS.split(",")
            if item.strip()
        }

        if extension in blocked:
            raise HTTPException(
                status_code=400,
                detail="File type is not allowed"
            )

        if not settings.CLAMSCAN_PATH:
            return

        result = subprocess.run(
            [settings.CLAMSCAN_PATH, "--no-summary", path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=400,
                detail="Malware scan failed"
            )
