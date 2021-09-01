# coding=utf-8
import os
import httpx

token = os.getenv("TgBOT_TOKEN")
assert token, "no TgBOT token provided"
print(f"token = {token!r}")


def api_call(method_name: str):
    url = f"https://api.telegram.org/bot{token}/{method_name}"

    response = httpx.post(url)
    return response.json()


def get_me():
    response = api_call("getMe")
    return response
