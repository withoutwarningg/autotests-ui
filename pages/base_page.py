from __future__ import annotations

from playwright.sync_api import Locator, Page


class BasePage:
    """Базовый класс для всех Page Object.

    Инкапсулирует то, что общее для любой страницы: открытие по
    относительному пути (абсолютный base_url задаётся один раз на уровне
    контекста браузера в conftest.py) и короткий алиас для локатора.
    Конкретные страницы (LoginPage, InventoryPage, ...) описывают только
    СВОИ локаторы и бизнес-действия поверх этого фундамента — сами тесты
    вообще не знают ни про Playwright, ни про CSS/data-test селекторы.
    """

    path: str = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> "BasePage":
        self.page.goto(self.path)
        return self

    def title(self) -> str:
        return self.page.title()

    @property
    def url(self) -> str:
        return self.page.url

    def _locator(self, selector: str) -> Locator:
        return self.page.locator(selector)
