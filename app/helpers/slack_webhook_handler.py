import asyncio
import json
import logging
import math
import time
import traceback
from typing import Optional

import httpx
from fastapi import Request

from app.core.configs import settings
from app.core.constants.messages import LogMessage

logger = logging.getLogger(__name__)


class SlackWebhookHelper:
    def __init__(self):
        self.webhook_url = settings.SLACK_HOOK_URL
        self.headers = {"Content-type": "application/json"}
        self.timeout_seconds = settings.SLACK_TIMEOUT_SECONDS
        self.max_retries = settings.SLACK_MAX_RETRIES
        self.retry_backoff_seconds = settings.SLACK_RETRY_BACKOFF_SECONDS

    async def send_slack(self, webhook_url: str, data: dict):
        timeout = httpx.Timeout(self.timeout_seconds)
        async with httpx.AsyncClient(timeout=timeout) as client:
            for attempt in range(1, self.max_retries + 2):
                try:
                    response = await client.post(webhook_url, data=data, headers=self.headers)
                    response.raise_for_status()
                    return
                except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError) as error:
                    if attempt >= self.max_retries + 1:
                        raise error
                    await asyncio.sleep(self.retry_backoff_seconds * attempt)

    @staticmethod
    def _extract_request_values(request: Optional[Request]) -> tuple[str, str, str]:
        method_value = LogMessage.NO_REQUEST.message
        path_value = LogMessage.NO_REQUEST.message
        request_id = LogMessage.NO_REQUEST.message
        if request:
            method_value = str(request.method).upper()
            path_value = str(request.url.path)
            request_id = str(getattr(request.state, "request_id", LogMessage.NO_REQUEST.message))
        return method_value, path_value, request_id

    def notify(self, status_code: int, message: str, level_error: str, request: Request = None):
        try:
            if not self.webhook_url:
                logger.info("Slack webhook URL is not set")
                return

            message_lite = (message[:100] + "...") if len(message) > 100 else message
            method_value, path_value, request_id = self._extract_request_values(request)

            project_name = settings.PROJECT_NAME
            env = settings.ENVIRONMENT
            try:
                subject = "[%s] [%s] %s: %s" % (
                    project_name,
                    env,
                    level_error,
                    message_lite,
                )

            except Exception:
                subject = "%s: %s" % (level_error, str(message_lite))

            attachments = [
                {
                    "color": "danger",
                    "title": subject,
                    "fields": [
                        {
                            "title": "Level",
                            "value": level_error,
                            "short": True,
                        },
                        {
                            "title": "Environment",
                            "value": env,
                            "short": True,
                        },
                        {
                            "title": "Method",
                            "value": method_value,
                            "short": True,
                        },
                        {
                            "title": "Error Code",
                            "value": status_code,
                            "short": True,
                        },
                        {
                            "title": "Path",
                            "value": "`{p}`".format(p=path_value),
                            "short": False,
                        },
                        {
                            "title": "Request ID",
                            "value": str(request_id),
                            "short": False,
                        },
                        {
                            "title": "Message",
                            "value": str(message),
                            "short": False,
                        },
                    ],
                    "footer": project_name,
                    "ts": int(time.time()),
                }
            ]

            """
            slack message attachment text has max of 8000 bytes
            lets split it up into 7900 bytes long chunks to be on the safe side
            """
            message_detail = traceback.format_exc(-10)
            if message_detail.strip() and message_detail.strip() != "NoneType: None":
                split = 7900
                parts = range(math.ceil(len(message_detail.encode("utf8")) / split))

                for part in parts:
                    start = 0 if part == 0 else split * part
                    end = split if part == 0 else split * part + split

                    """
                    combine final text and prepend it with line breaks
                    so the details in slack message will fully collapse
                    """
                    detail_text = "\r\n\r\n\r\n\r\n\r\n\r\n\r\n" + message_detail[start:end]

                    title = "Message details"
                    if part > 0:
                        title = "Message details (Part {})".format(part + 1)

                    attachments.append(
                        {
                            "color": "danger",
                            "title": title,
                            "text": detail_text,
                            "ts": time.time(),
                        }
                    )

            data = {
                "payload": json.dumps({"attachments": attachments}),
            }

            # Schedule non-blocking send on running loop.
            try:
                loop = asyncio.get_running_loop()
                task = loop.create_task(self.send_slack(self.webhook_url, data=data))
                task.add_done_callback(
                    lambda t: logger.exception(t.exception())
                    if t.exception()
                    else None
                )
            except RuntimeError:
                # Fallback for contexts without a running loop.
                asyncio.run(self.send_slack(self.webhook_url, data=data))

        except Exception as e:
            logger.exception(e)
