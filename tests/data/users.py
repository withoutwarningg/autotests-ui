from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SauceUser:
    """Один из встроенных тестовых пользователей saucedemo.com.

    Пароль у всех пользователей один и тот же (secret_sauce) — это не
    секрет, а официально задокументированная прямо на странице логина
    тестовая учётка, поэтому её можно спокойно хранить в коде.
    """

    username: str
    password: str = "secret_sauce"


STANDARD_USER = SauceUser("standard_user")
LOCKED_OUT_USER = SauceUser("locked_out_user")
PROBLEM_USER = SauceUser("problem_user")
PERFORMANCE_GLITCH_USER = SauceUser("performance_glitch_user")
ERROR_USER = SauceUser("error_user")
VISUAL_USER = SauceUser("visual_user")
