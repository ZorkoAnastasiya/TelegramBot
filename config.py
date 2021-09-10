from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    bot_token: str = Field(..., env="TgBOT_TOKEN")
    webhook_secret: str = Field(..., env="WEBHOOK_SECRET")
    x_secret_key: str = Field(..., env="X_SECRET_KEY")
    basic_key: str = Field(..., env="BASIC_KEY")


@property
def bot_url(self):
    return f"https://api.telegram.org/bot{self.bot_token}"


@property
def webhook_path(self):
    return f"/tg/web{self.webhook_secret}"


settings = Settings()
