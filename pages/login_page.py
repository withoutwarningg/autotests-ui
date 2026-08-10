from __future__ import annotations

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница логина (главная страница saucedemo.com)."""

    path = "/"

    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def login(self, username: str, password: str) -> "LoginPage":
        """Заполняет форму логина и жмёт кнопку входа.

        Возвращает саму себя, а не InventoryPage: логин может как удаться
        (и тогда браузер окажется на /inventory.html), так и не удаться
        (тогда мы остаёмся на странице логина с сообщением об ошибке) —
        какой из этих исходов правильный, решает тест, а не Page Object.
        """
        self._locator(self.USERNAME_INPUT).fill(username)
        self._locator(self.PASSWORD_INPUT).fill(password)
        self._locator(self.LOGIN_BUTTON).click()
        return self

    def get_error_message(self) -> str:
        return self._locator(self.ERROR_MESSAGE).inner_text()

    def has_error(self) -> bool:
        return self._locator(self.ERROR_MESSAGE).count() > 0

    def is_login_form_visible(self) -> bool:
        return self._locator(self.LOGIN_BUTTON).is_visible()
