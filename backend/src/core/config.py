import os


class Settings:
    app_name: str = os.getenv("APP_NAME", "Lab Python Utilities API")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    @property
    def cors_origins(self) -> list[str]:
        origins = self.frontend_origin.split(",")
        return [origin.strip() for origin in origins if origin.strip()]


settings = Settings()
