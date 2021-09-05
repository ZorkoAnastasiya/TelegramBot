# coding=utf-8
import hmac
import httpx

from config import settings
from fastapi import HTTPException
from TgBot.type_bot import *


rr_type_map = {
    "getMe": GetMeResponse,
    "getWebhookInfo": GetWebhookInfoResponse,
    "setWebhook": SetWebhookResponse,
    "sendMessage": SendMessageResponse
}


async def telegram_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient(base_url = settings.bot_url) as client:
        yield client


async def api_call(
        client: httpx.AsyncClient,
        method_name: str,
        data: Optional[Type] = None
):
    rr_type = rr_type_map[method_name]
    payload = data.dict(exclude_unset = True) if data is not None else None,
    response: httpx.Response = await client.post(f"/{method_name}", json=payload)
    raw_response = response.json()
    result = rr_type.parse_obj(raw_response)

    return result


async def get_me(client: httpx.AsyncClient) -> User:
    response = await api_call(client, "getMe")
    return response.result


async def get_webhook_info(client: httpx.AsyncClient) -> WebhookInfo:
    response = await api_call(client, "getWebhookInfo")
    return response.result


async def set_webhook(
        client: httpx.AsyncClient,
        whi: WebhookInfo
) ->bool:
    response = await api_call(client, "setWebhook", data = whi)
    return response.result


async def send_message(
        client: httpx.AsyncClient,
        request: SendMessageRequest
) -> Message:
    response = await api_call(client, "sendMessage", data = request)
    return response.result


def authorize(key_1, key_2) ->None:
    exception = HTTPException(status_code=404, detail="not found")
    if not (key_1 and key_2):
        raise exception
    if not (settings.basic_key and settings.x_secret_key):
        raise exception
    compare_key_1 = hmac.compare_digest(key_1, settings.basic_key)
    compare_key_2 = hmac.compare_digest(key_2, settings.x_secret_key)
    if not (compare_key_1 and compare_key_2):
        raise exception


def hide_webhook_secret(whi) -> None:
    if not (whi and whi.url):
        return
    whi.url = whi.url.replace(settings.webhook_secret, "***")
