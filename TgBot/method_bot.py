# coding=utf-8
import httpx
from config import settings
from TgBot.type_bot import *


async def telegram_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient(base_url = settings.bot_url) as client:
        yield client


rr_type_map = {
    "getMe": GetMeResponse,
    "getWebhookInfo": GetWebhookInfoResponse,
    "setWebhook": SetWebhookResponse,
    "sendMessage": SendMessageResponse
}


async def api_call(
        client: httpx.AsyncClient,
        method_name: str,
        data: Optional[Type] = None
) -> Response:
    rr_type = rr_type_map[method_name]
    payload = data.dict(exclude_unset = True) if data is not None else None,
    print(f"api_call: payload - {payload}")
    response: httpx.Response = await client.post(f"/{method_name}", json=payload)
    raw_response = response.json()
    print(f"api_call: raw_response - {raw_response}")
    result = rr_type.parse_obj(raw_response)
    print(f"api_call: result - {result}")

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
    response = await api_call(client, "setWebhook", data=whi)
    return response.result


async def send_message(
        client: httpx.AsyncClient,
        request: SendMessageRequest
) -> Message:
    print(f"send_message: request - {request}")
    response = await api_call(client, "sendMessage", data=request)
    print(f"send_message: response.result - {response.result}")
    print(f"send_message: response.dict - {response.json()}")
    return response.result
