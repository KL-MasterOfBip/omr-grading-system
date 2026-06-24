from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # ── Ứng dụng ──────────────────────────────────────────
    APP_NAME: str = "Hệ thống chấm điểm trắc nghiệm"
    DEBUG: bool = True

    # ── Database ───────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./omr.db"

    # ── JWT ────────────────────────────────────────────────
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24   # 1 ngày

    # ── Upload ─────────────────────────────────────────────
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10

    # ── OMR ────────────────────────────────────────────────
    OMR_NUM_QUESTIONS: int = 40
    OMR_NUM_CHOICES: int = 4

    class Config:
        env_file = ".env"           # đọc từ file .env nếu có
        env_file_encoding = "utf-8"


@lru_cache()             # chỉ khởi tạo Settings 1 lần, dùng lại ở mọi nơi
def get_settings() -> Settings:
    return Settings()


settings = get_settings()