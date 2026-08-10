from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage


@allure.feature("Оформление заказа")
class TestCheckout:
    @pytest.mark.smoke
    def test_full_checkout_flow_completes_successfully(self, logged_in_page: InventoryPage) -> None:
        logged_in_page.add_to_cart("Sauce Labs Backpack")
        cart_page = logged_in_page.open_cart()

        step_one = cart_page.checkout()
        step_one.fill_info("Ilya", "Doronin", "185000")
        step_two = step_one.continue_to_overview()

        assert step_two.get_item_count() == 1

        complete_page = step_two.finish()

        assert complete_page.get_confirmation_message() == "Thank you for your order!"
        assert "/checkout-complete.html" in complete_page.url

    @pytest.mark.regression
    def test_order_total_equals_subtotal_plus_tax(self, logged_in_page: InventoryPage) -> None:
        logged_in_page.add_to_cart("Sauce Labs Backpack")
        cart_page = logged_in_page.open_cart()

        step_one = cart_page.checkout()
        step_one.fill_info("Ilya", "Doronin", "185000")
        step_two = step_one.continue_to_overview()

        subtotal = step_two.get_subtotal()
        tax = step_two.get_tax()
        total = step_two.get_total()

        assert round(subtotal + tax, 2) == total

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "first_name, last_name, postal_code, missing_field",
        [
            pytest.param("", "Doronin", "185000", "First Name", id="missing-first-name"),
            pytest.param("Ilya", "", "185000", "Last Name", id="missing-last-name"),
            pytest.param("Ilya", "Doronin", "", "Postal Code", id="missing-postal-code"),
        ],
    )
    def test_checkout_requires_all_fields(
        self,
        logged_in_page: InventoryPage,
        first_name: str,
        last_name: str,
        postal_code: str,
        missing_field: str,
    ) -> None:
        logged_in_page.add_to_cart("Sauce Labs Backpack")
        cart_page = logged_in_page.open_cart()
        step_one = cart_page.checkout()

        step_one.fill_info(first_name, last_name, postal_code)
        step_one.continue_to_overview()  # уходит на step-two.html только при успехе

        assert step_one.has_error()
        assert missing_field in step_one.get_error_message()
        assert "/checkout-step-one.html" in step_one.url
