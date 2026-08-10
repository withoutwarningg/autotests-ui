from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.data.users import (
    ERROR_USER,
    LOCKED_OUT_USER,
    PERFORMANCE_GLITCH_USER,
    PROBLEM_USER,
    STANDARD_USER,
    SauceUser,
)


@allure.feature("Логин")
class TestLogin:
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "user",
        [STANDARD_USER, PROBLEM_USER, PERFORMANCE_GLITCH_USER, ERROR_USER],
        ids=lambda u: u.username,
    )
    def test_valid_user_can_login(self, login_page: LoginPage, user: SauceUser) -> None:
        login_page.login(user.username, user.password)

        inventory_page = InventoryPage(login_page.page)
        assert "/inventory.html" in inventory_page.url
        assert not login_page.has_error()

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "username, password, expected_message",
        [
            pytest.param(
                LOCKED_OUT_USER.username,
                LOCKED_OUT_USER.password,
                "Epic sadface: Sorry, this user has been locked out.",
                id="locked-out-user",
            ),
            pytest.param(
                STANDARD_USER.username,
                "wrong_password",
                "Epic sadface: Username and password do not match any user in this service",
                id="wrong-password",
            ),
            pytest.param(
                "",
                "",
                "Epic sadface: Username is required",
                id="empty-credentials",
            ),
            pytest.param(
                STANDARD_USER.username,
                "",
                "Epic sadface: Password is required",
                id="missing-password",
            ),
        ],
    )
    def test_invalid_login_shows_expected_error(
        self, login_page: LoginPage, username: str, password: str, expected_message: str
    ) -> None:
        login_page.login(username, password)

        assert login_page.has_error()
        assert login_page.get_error_message() == expected_message
        assert "/inventory.html" not in login_page.url

    @pytest.mark.smoke
    def test_logout_returns_to_login_page(self, logged_in_page: InventoryPage) -> None:
        login_page = logged_in_page.logout()

        assert login_page.url.rstrip("/") == "https://www.saucedemo.com"
        assert login_page.is_login_form_visible()
