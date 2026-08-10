from __future__ import annotations

from playwright.sync_api import Locator

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Страница каталога товаров (/inventory.html)."""

    path = "/inventory.html"

    ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    SORT_SELECT = "[data-test='product-sort-container']"
    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def item_by_name(self, name: str) -> Locator:
        """Карточка товара, содержащая указанное имя."""
        return self._locator(self.ITEM).filter(has_text=name)

    def add_to_cart(self, item_name: str) -> "InventoryPage":
        self.item_by_name(item_name).locator("button").click()
        return self

    def get_item_names(self) -> list[str]:
        return self._locator(self.ITEM_NAME).all_inner_texts()

    def get_item_prices(self) -> list[float]:
        raw_prices = self._locator(self.ITEM_PRICE).all_inner_texts()
        return [float(price.replace("$", "")) for price in raw_prices]

    def sort_by(self, option_value: str) -> "InventoryPage":
        """option_value — одно из: az, za, lohi, hilo (значения <option> сортировки)."""
        self._locator(self.SORT_SELECT).select_option(option_value)
        return self

    def get_cart_count(self) -> int:
        badge = self._locator(self.CART_BADGE)
        if badge.count() == 0:
            return 0
        return int(badge.inner_text())

    def open_cart(self) -> "CartPage":
        from pages.cart_page import CartPage  # локальный импорт — избегаем цикла между модулями страниц

        self._locator(self.CART_LINK).click()
        return CartPage(self.page)

    def logout(self) -> "LoginPage":
        from pages.login_page import LoginPage

        self._locator(self.BURGER_MENU_BUTTON).click()
        self._locator(self.LOGOUT_LINK).click()
        return LoginPage(self.page)
