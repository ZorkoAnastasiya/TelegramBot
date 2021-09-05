from fastapi import Depends
from .type_bot import *
from .method_bot import *

Telegram = Depends(telegram_client)
