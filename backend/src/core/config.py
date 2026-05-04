import os
from pathlib import Path


def load_local_env() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        cleaned = line.strip()

        if not cleaned or cleaned.startswith("#") or "=" not in cleaned:
            continue

        key, value = cleaned.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_local_env()


class Settings:
    app_name: str = os.getenv("APP_NAME", "Lab Python Utilities API")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    @property
    def cors_origins(self) -> list[str]:
        origins = self.frontend_origin.split(",")
        return [origin.strip() for origin in origins if origin.strip()]


settings = Settings()
