# coding=utf-8
import TelegramBot
from fastapi import FastAPI, Header
from typing import Optional


app = FastAPI()


@app.get("/tg/about")
async def _():
    user = TelegramBot.get_me()
    return user


@app.get("/tg/webhook")
async def _():
    whi = TelegramBot.get_webhook_info()
    return whi


@app.post("/tg/webhook")
async def _(
        whi: TelegramBot.WebhookInfo,
        x_secret_key: Optional[str] = Header(None),
        authorization: Optional[str] = Header(None)
):
    key = TelegramBot.key_verification(x_secret_key)
    if not key:
        return {"Message": "No access"}
    else:
        auth = TelegramBot.entrance(authorization)
        if not auth:
            return {"Message": "No rights"}
        else:
            result = TelegramBot.set_webhook(whi)
            return result
