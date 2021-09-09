# coding=utf-8
import json
import httpx
from fastapi import Body
from config import settings
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
) -> Response:
    rr_type = rr_type_map[method_name]
    payload = data.dict(exclude_unset=True) if data is not None else None
    response: httpx.Response = await client.post(f"/{method_name}", json=payload)
    raw_response = response.json()
    print(f"api_call: raw_response - {raw_response}")
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
    response = await api_call(client, "setWebhook", data=whi)
    return response.result


async def send_message(
        client: httpx.AsyncClient,
        request: SendMessageRequest
) -> Message:
    response = await api_call(client, "sendMessage", data=request)
    return response.result


async def get_numbers(user: str, number: str):
    async with httpx.AsyncClient(base_url = "https://teach-python.herokuapp.com") as client:
        cookies = {"user": user}
        response = await client.post("/task_numbers", cookies=cookies, json=number)

        print(f"get_numbers: response.json - {response}")
        return response.json()


async def parser_text(update: Update = Body(...)):
    user = str(update.message.chat.id)
    text = update.message.text.lower()
    print(f"parser: user - {user}, text - {text}")
    if text == "/start":
        return "Давай начнем! Введи число! Или слово stop!"
    elif text == "stop":
        print(f"parser - text - {text!r}")
        msg = json.dumps(text)
        print(f"parser - msg - {msg!r}")
        number = await get_numbers(user, msg)
        return f"Сумма твоих чисел {number}!"
    elif text.isdigit():
        if int(text) > 4294967295:
            return "Слишком большое число!"
        else:
            number = await get_numbers(user, text)
            print(f"parser - number - {number}")
            return f"Ок! Ты ввел число {int(text)}!"
    else:
        return "bla-bla-bla - непонимаю тебя!"
