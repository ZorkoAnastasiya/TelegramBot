# coding=utf-8
import TelegramBot
from fastapi import FastAPI

app = FastAPI()


@app.get("/tb/about")
def _():
    response = TelegramBot.get_me()
    return response
