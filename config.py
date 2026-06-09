import os
from dataclasses import dataclass
from datetime import time
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Settings:
    account_number: str
    app_key: str
    app_secret: str
    product_code: str
    symbol: str
    api_domain: str
    token_cache_path: Path
    buy_offset: int
    sell_offset: int
    polling_interval_seconds: int
    trading_start: time
    trading_end: time

    @classmethod
    def load(cls) -> "Settings":
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            with env_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, val = line.split("=", 1)
                        key = key.strip()
                        val = val.strip().strip("'\"")
                        if key:
                            os.environ[key] = val

        account_number = (
            os.environ.get("GH_ACCOUNT", "")
            or os.environ.get("ACCOUNT_NUMBER", "")
        ).strip()
        app_key = os.environ.get("GH_APPKEY", "").strip()
        app_secret = os.environ.get("GH_APPSECRET", "").strip()
        product_code = (
            os.environ.get("GH_PRODUCT_CODE", "")
            or os.environ.get("PRODUCT_CODE", "01")
        ).strip() or "01"

        missing = [name for name, value in (
            ("GH_ACCOUNT / ACCOUNT_NUMBER", account_number),
            ("GH_APPKEY", app_key),
            ("GH_APPSECRET", app_secret),
        ) if not value]

        if missing:
            raise EnvironmentError(
                "Missing required environment variables: " + ", ".join(missing)
            )

        api_domain = (
            os.environ.get("GH_API_DOMAIN", "")
            or os.environ.get("API_DOMAIN", "")
            or "https://openapivts.koreainvestment.com:29443"
        ).strip()

        return cls(
            account_number=account_number,
            app_key=app_key,
            app_secret=app_secret,
            product_code=product_code,
            symbol="005930",
            api_domain=api_domain,
            token_cache_path=Path(__file__).parent / "token_cache.json",
            buy_offset=-2000,
            sell_offset=2000,
            polling_interval_seconds=120,
            trading_start=time(hour=9, minute=10),
            trading_end=time(hour=15, minute=30),
        )

    def get_auth_url(self) -> str:
        return f"{self.api_domain}/oauth2/tokenP"
