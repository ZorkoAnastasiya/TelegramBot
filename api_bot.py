# coding=utf-8
import traceback
import httpx
import TgBot

from config import settings
from fastapi import FastAPI, Header, Body
from typing import Optional


app = FastAPI()


@app.get("/tg/about")
async def _(client: httpx.AsyncClient = TgBot.Telegram):
    user = await TgBot.get_me(client)
    return user


@app.get("/tg/webhook")
async def _(client: httpx.AsyncClient = TgBot.Telegram):
    whi = await TgBot.get_webhook_info(client)
    TgBot.hide_webhook_secret(whi)
    return whi


@app.post("/tg/webhook")
async def _(
        client: httpx.AsyncClient = TgBot.Telegram,
        whi: TgBot.WebhookInfo = Body(...),
        authorization: Optional[str] = Header(None),
        x_secret_key: Optional[str] = Header(None),

):
    TgBot.authorize(authorization, x_secret_key)
    whi.url = f"{whi.url}{settings.webhook_path}"
    webhook_set = await TgBot.set_webhook(client, whi)
    whi = await TgBot.get_webhook_info(client)
    TgBot.hide_webhook_secret(whi)

    return {
        "ok": webhook_set,
        "webhook": whi
    }


@app.post(settings.webhook_path)
async def _(
        client: httpx.AsyncClient = TgBot.Telegram,
        update: TgBot.Update = Body(...)
):
    try:
        await TgBot.send_message(
            client,
            TgBot.SendMessageRequest(
                chat_id=update.message.chat.id,
                reply_to_message=update.message.message_id,
                text=update.json()
            )
        )
    except Exception:
        traceback.print_exc()
