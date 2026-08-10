from __future__ import annotations

import allure
import pytest

from pages.inventory_page import InventoryPage


@allure.feature("Каталог товаров")
class TestInventory:
    @pytest.mark.smoke
    def test_inventory_page_shows_six_items(self, logged_in_page: InventoryPage) -> None:
        assert len(logged_in_page.get_item_names()) == 6

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "sort_option, expected_order",
        [
            pytest.param("az", "asc_name", id="name-a-to-z"),
            pytest.param("za", "desc_name", id="name-z-to-a"),
            pytest.param("lohi", "asc_price", id="price-low-to-high"),
            pytest.param("hilo", "desc_price", id="price-high-to-low"),
        ],
    )
    def test_sorting_orders_items_correctly(
        self, logged_in_page: InventoryPage, sort_option: str, expected_order: str
    ) -> None:
        logged_in_page.sort_by(sort_option)

        if expected_order == "asc_name":
            names = logged_in_page.get_item_names()
            assert names == sorted(names)
        elif expected_order == "desc_name":
            names = logged_in_page.get_item_names()
            assert names == sorted(names, reverse=True)
        elif expected_order == "asc_price":
            prices = logged_in_page.get_item_prices()
            assert prices == sorted(prices)
        elif expected_order == "desc_price":
            prices = logged_in_page.get_item_prices()
            assert prices == sorted(prices, reverse=True)

    @pytest.mark.smoke
    def test_adding_item_to_cart_updates_badge(self, logged_in_page: InventoryPage) -> None:
        assert logged_in_page.get_cart_count() == 0

        logged_in_page.add_to_cart("Sauce Labs Backpack")

        assert logged_in_page.get_cart_count() == 1

    @pytest.mark.regression
    def test_adding_multiple_items_to_cart_increments_badge(self, logged_in_page: InventoryPage) -> None:
        for item_name in ("Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"):
            logged_in_page.add_to_cart(item_name)

        assert logged_in_page.get_cart_count() == 3

    @pytest.mark.regression
    def test_cart_page_lists_added_item(self, logged_in_page: InventoryPage) -> None:
        logged_in_page.add_to_cart("Sauce Labs Backpack")

        cart_page = logged_in_page.open_cart()

        assert cart_page.get_item_count() == 1
        assert "Sauce Labs Backpack" in cart_page.get_item_names()
