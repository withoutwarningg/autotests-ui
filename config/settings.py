from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Подхватываем локальный .env, если он есть (в репозиторий не коммитится,
# см. .gitignore). Переменные окружения имеют приоритет над файлом.
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)


@dataclass(frozen=True)
class Settings:
    """Настройки прогона, полностью управляемые переменными окружения.

    Ничего не захардкожено ни в тестах, ни в Page Object — благодаря этому
    один и тот же код можно направить на другой стенд, просто переопределив
    переменную окружения, не трогая ни строчки в остальном фреймворке.
    """

    base_url: str = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
    default_timeout_ms: int = int(os.getenv("UI_TIMEOUT_MS", "10000"))


settings = Settings()
