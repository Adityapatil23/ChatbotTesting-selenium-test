import pytest
from pages.login_page import LoginPage
from utils.db_utils import DatabaseUtils
import allure

@allure.epic("VWO Login Tests")
@allure.feature("Login Functionality")
class TestLoginPOM:

    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.login_page = LoginPage(driver)
        self.db_utils = DatabaseUtils()

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_valid_login(self):
        """Test login with valid credentials"""
        with allure.step("Navigate to login page"):
            self.login_page.navigate_to()
            assert self.login_page.is_login_page_displayed(), "Login page is not displayed"

        with allure.step("Login with valid credentials"):
            valid_user = self.config['test_data']['valid_user']
            self.login_page.login(valid_user['email'], valid_user['password'])
            
            # Verify user exists in database
            assert self.db_utils.verify_user_exists(valid_user['email']), "User not found in database"

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        with allure.step("Navigate to login page"):
            self.login_page.navigate_to()
            assert self.login_page.is_login_page_displayed(), "Login page is not displayed"

        with allure.step("Login with invalid credentials"):
            invalid_user = self.config['test_data']['invalid_user']
            self.login_page.login(invalid_user['email'], invalid_user['password'])
            
            # Verify error message
            error_message = self.login_page.get_error_message()
            assert error_message is not None, "Error message not displayed"
            assert "Invalid email or password" in error_message, "Incorrect error message"

    @allure.story("Remember Me Functionality")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_remember_me(self):
        """Test remember me functionality"""
        with allure.step("Navigate to login page"):
            self.login_page.navigate_to()
            assert self.login_page.is_login_page_displayed(), "Login page is not displayed"

        with allure.step("Login with remember me checked"):
            valid_user = self.config['test_data']['valid_user']
            self.login_page.login(valid_user['email'], valid_user['password'], remember_me=True)
            
            # Verify user exists in database
            assert self.db_utils.verify_user_exists(valid_user['email']), "User not found in database"

    @allure.story("Forgot Password Link")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_forgot_password_link(self):
        """Test forgot password link functionality"""
        with allure.step("Navigate to login page"):
            self.login_page.navigate_to()
            assert self.login_page.is_login_page_displayed(), "Login page is not displayed"

        with allure.step("Click forgot password link"):
            self.login_page.click_forgot_password()
            # Add assertions for forgot password page if needed 