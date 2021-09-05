import os

bot_token = os.getenv("TgBOT_TOKEN")
assert bot_token, "in environment variable TgBOT_TOKEN is not set"
print(f"bot_token = {bot_token!r}")
bot_url = f"https://api.telegram.org/bot{bot_token}"
print(f"{bot_url!r}")


webhook_secret = os.getenv("WEBHOOK_SECRET")
assert webhook_secret, "in environment variable WEBHOOK_SECRET is not set"
webhook_path = f"/tg/web{webhook_secret}"
print(f"{webhook_path!r}")

x_secret_key = os.getenv("X_SECRET_KEY")
assert x_secret_key, "in environment variable X_SECRET_KEY is not set"
print(f"{x_secret_key!r}")
basic_key = os.getenv("BASIC_KEY")
assert basic_key, "in environment variable BASIC_KEY is not set"
print(f"{basic_key!r}")


class Settings:
    bot_token = bot_token
    bot_url = bot_url
    webhook_secret = webhook_secret
    webhook_path = webhook_path
    x_secret_key = x_secret_key
    basic_key = basic_key


settings = Settings()
