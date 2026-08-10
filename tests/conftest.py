from __future__ import annotations

from typing import Iterator

import allure
import pytest
from playwright.sync_api import Page

from config.settings import settings
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.data.users import STANDARD_USER


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Прокидываем базовый URL стенда во все контексты браузера.

    После этого Page Object открывают страницы по относительному пути
    (BasePage.open() делает просто page.goto(self.path)) — сам стенд
    настраивается в одном месте и переопределяется через UI_BASE_URL.
    """
    return {**browser_context_args, "base_url": settings.base_url}


@pytest.fixture(autouse=True)
def _default_timeout(page: Page) -> None:
    """Единый таймаут ожидания элементов для всех тестов, настраиваемый через UI_TIMEOUT_MS."""
    page.set_default_timeout(settings.default_timeout_ms)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Открытая страница логина — стартовая точка почти любого UI-теста."""
    return LoginPage(page).open()


@pytest.fixture
def logged_in_page(page: Page) -> Iterator[InventoryPage]:
    """Каталог товаров сразу после успешного логина стандартным пользователем.

    Нужна тестам, для которых сам процесс логина не является предметом
    проверки (сортировка, корзина, чекаут) — чтобы не дублировать в каждом
    таком тесте одни и те же три строчки логина.
    """
    with allure.step(f"Логин под пользователем {STANDARD_USER.username}"):
        LoginPage(page).open().login(STANDARD_USER.username, STANDARD_USER.password)
    yield InventoryPage(page)
