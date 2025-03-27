import pytest
from pages.login_page import LoginPage
import allure

@allure.epic("VWO Login Tests")
@allure.feature("Login Functionality")
class TestLoginPOM:

    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.login_page = LoginPage(driver)

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_valid_login(self):
        """Test login with valid credentials"""
        with allure.step("Navigate to login page"):
            self.login_page.navigate_to()
            assert self.login_page.is_login_page_displayed(), "Login page is not displayed"
            
            # Verify form labels
            assert self.login_page.get_email_label_text() == "Email", "Incorrect email label"
            assert self.login_page.get_password_label_text() == "Password", "Incorrect password label"

        with allure.step("Login with valid credentials"):
            valid_user = self.config['test_data']['valid_user']
            self.login_page.login(valid_user['email'], valid_user['password'])
            
            # Verify successful login
            assert self.login_page.is_dashboard_displayed(), "Dashboard not displayed after login"

        with allure.step("Logout"):
            self.login_page.logout()
            assert self.login_page.is_logged_out(), "Logout failed"

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
            
            # Verify successful login
            assert self.login_page.is_dashboard_displayed(), "Dashboard not displayed after login"
            
            # Verify remember me is checked
            assert self.login_page.is_remember_me_checked(), "Remember me checkbox not checked"

        with allure.step("Logout"):
            self.login_page.logout()
            assert self.login_page.is_logged_out(), "Logout failed"

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
            # Verify forgot password page is displayed
            assert self.login_page.is_forgot_password_page_displayed(), "Forgot password page not displayed" 