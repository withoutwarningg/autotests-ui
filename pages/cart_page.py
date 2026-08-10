from __future__ import annotations

from pages.base_page import BasePage


class CartPage(BasePage):
    """Страница корзины (/cart.html)."""

    path = "/cart.html"

    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CHECKOUT_BUTTON = "[data-test='checkout']"

    def get_item_names(self) -> list[str]:
        return self._locator(self.CART_ITEM_NAME).all_inner_texts()

    def get_item_count(self) -> int:
        return self._locator(self.CART_ITEM).count()

    def checkout(self) -> "CheckoutStepOnePage":
        from pages.checkout_page import CheckoutStepOnePage

        self._locator(self.CHECKOUT_BUTTON).click()
        return CheckoutStepOnePage(self.page)
