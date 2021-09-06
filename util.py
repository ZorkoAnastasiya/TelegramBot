import hmac
from fastapi import HTTPException
from config import settings


def update_forward_refs(klass):
    klass.update_forward_refs()
    return klass


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

