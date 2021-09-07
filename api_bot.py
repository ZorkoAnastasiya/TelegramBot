# coding=utf-8
import traceback
import httpx
import TgBot
import util
from config import settings
from fastapi import FastAPI, Header, Body
from typing import Optional


app = FastAPI()


@app.get("/")
async def _():
    return "Telegram Bot"


@app.get("/tg/about")
async def _(client: httpx.AsyncClient = TgBot.Telegram):
    user = await TgBot.get_me(client)
    return user


@app.get("/tg/webhook")
async def _(client: httpx.AsyncClient = TgBot.Telegram):
    whi = await TgBot.get_webhook_info(client)
    util.hide_webhook_secret(whi)
    return whi


@app.post("/tg/webhook")
async def _(
        client: httpx.AsyncClient = TgBot.Telegram,
        whi: TgBot.WebhookInfo = Body(...),
        authorization: Optional[str] = Header(None),
        x_secret_key: Optional[str] = Header(None),

):
    util.authorize(authorization, x_secret_key)

    whi.url = f"{whi.url}{settings.webhook_path}"
    webhook_set = await TgBot.set_webhook(client, whi)

    whi = await TgBot.get_webhook_info(client)
    util.hide_webhook_secret(whi)

    return {
        "ok": webhook_set,
        "webhook": whi
    }


@app.post(settings.webhook_path)
async def _(
        client: httpx.AsyncClient = TgBot.Telegram,
        update: TgBot.Update = Body(...)
):
    # noinspection PyBroadException
    try:
        await TgBot.send_message(
            client,
            TgBot.SendMessageRequest(
                chat_id=update.message.chat.id,
                reply_to_message_id=update.message.message_id,
                text="bla-bla-bla"
            )
        )
    except Exception:
        traceback.print_exc()
