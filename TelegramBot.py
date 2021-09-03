# coding=utf-8
import os
import httpx
from pydantic import BaseModel, Field
from typing import Optional


token = os.getenv("TgBOT_TOKEN")
assert token, "no TgBOT token provided"
print(f"token = {token!r}")


class User(BaseModel):
    id: int = Field(...)
    is_bot: bool = Field(...)
    first_name: str = Field(...)
    last_name: str = Field('')
    username: str = Field('')


class WebhookInfo(BaseModel):
    url: str
    pending_update_count: int = 0
    last_error_date: int = 0
    last_error_message: str = ''


class GetMeResponse(BaseModel):
    ok: bool
    result: Optional[User] = None
    error_code: int = 0
    description: str = ''


class WebhookInfoResponse(BaseModel):
    ok: bool
    result: Optional[WebhookInfo] = None
    error_code: int = 0
    description: str = ''


def api_call(method_name: str, payload=None):
    url = f"https://api.telegram.org/bot{token}/{method_name}"
    if payload:
        response = httpx.post(url, json=payload)
    else:
        response = httpx.post(url)
    return response.json()


def get_me() -> User:
    raw_response = api_call("getMe")
    response: GetMeResponse = GetMeResponse.parse_obj(raw_response)
    return response.result


def get_webhook_info() -> WebhookInfo:
    raw_response = api_call("getWebhookInfo")
    response: WebhookInfoResponse = WebhookInfoResponse.parse_obj(raw_response)
    return response.result


def set_webhook(whi: WebhookInfo):
    result = api_call("setWebhook", whi.dict())
    return result


def key_verification(x_secret_key: Optional[str]) -> bool:
    key = os.getenv("X_SECRET_KEY")
    return x_secret_key == key


def entrance(authorization: Optional[str]) ->bool:
    auth = os.getenv("BASIC_KEY")
    return authorization == auth
