from __future__ import annotations

from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    """Первый шаг оформления заказа — данные покупателя (/checkout-step-one.html)."""

    path = "/checkout-step-one.html"

    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    ERROR_MESSAGE = "[data-test='error']"

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutStepOnePage":
        self._locator(self.FIRST_NAME_INPUT).fill(first_name)
        self._locator(self.LAST_NAME_INPUT).fill(last_name)
        self._locator(self.POSTAL_CODE_INPUT).fill(postal_code)
        return self

    def continue_to_overview(self) -> "CheckoutStepTwoPage":
        self._locator(self.CONTINUE_BUTTON).click()
        return CheckoutStepTwoPage(self.page)

    def get_error_message(self) -> str:
        return self._locator(self.ERROR_MESSAGE).inner_text()

    def has_error(self) -> bool:
        return self._locator(self.ERROR_MESSAGE).count() > 0


class CheckoutStepTwoPage(BasePage):
    """Второй шаг — обзор заказа перед подтверждением (/checkout-step-two.html)."""

    path = "/checkout-step-two.html"

    CART_ITEM = ".cart_item"
    SUBTOTAL_LABEL = "[data-test='subtotal-label']"
    TAX_LABEL = "[data-test='tax-label']"
    TOTAL_LABEL = "[data-test='total-label']"
    FINISH_BUTTON = "[data-test='finish']"

    def get_item_count(self) -> int:
        return self._locator(self.CART_ITEM).count()

    def get_subtotal(self) -> float:
        return self._parse_amount(self._locator(self.SUBTOTAL_LABEL).inner_text())

    def get_tax(self) -> float:
        return self._parse_amount(self._locator(self.TAX_LABEL).inner_text())

    def get_total(self) -> float:
        return self._parse_amount(self._locator(self.TOTAL_LABEL).inner_text())

    @staticmethod
    def _parse_amount(label_text: str) -> float:
        # Например: "Item total: $29.99" -> 29.99
        return float(label_text.split("$")[-1])

    def finish(self) -> "CheckoutCompletePage":
        self._locator(self.FINISH_BUTTON).click()
        return CheckoutCompletePage(self.page)


class CheckoutCompletePage(BasePage):
    """Финальная страница подтверждения заказа (/checkout-complete.html)."""

    path = "/checkout-complete.html"

    COMPLETE_HEADER = ".complete-header"

    def get_confirmation_message(self) -> str:
        return self._locator(self.COMPLETE_HEADER).inner_text()
