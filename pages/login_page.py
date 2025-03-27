from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.ID, "login-username")
    PASSWORD_INPUT = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "js-login-btn")
    ERROR_MESSAGE = (By.ID, "js-notification-box-msg")
    REMEMBER_ME_CHECKBOX = (By.ID, "js-remember-me")
    FORGOT_PASSWORD_LINK = (By.ID, "js-forgot-password")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    FORGOT_PASSWORD_FORM = (By.ID, "js-forgot-password-form")
    EMAIL_LABEL = (By.CSS_SELECTOR, "label[for='login-username']")
    PASSWORD_LABEL = (By.CSS_SELECTOR, "label[for='login-password']")
    LOGIN_FORM = (By.ID, "js-login-form")
    USER_MENU = (By.ID, "js-user-menu")
    LOGOUT_BUTTON = (By.ID, "js-logout-btn")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = self.config['urls']['login_url']

    def navigate_to(self):
        """Navigate to login page"""
        self.driver.get(self.url)
        self.logger.info("Navigated to login page")

    def login(self, email, password, remember_me=False):
        """Login with given credentials"""
        try:
            self.send_keys(self.EMAIL_INPUT, email)
            self.send_keys(self.PASSWORD_INPUT, password)
            
            if remember_me:
                self.click_element(self.REMEMBER_ME_CHECKBOX)
            
            self.click_element(self.LOGIN_BUTTON)
            self.logger.info(f"Attempted login with email: {email}")
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            raise e

    def get_error_message(self):
        """Get error message if login fails"""
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except Exception as e:
            self.logger.error(f"Failed to get error message: {str(e)}")
            return None

    def click_forgot_password(self):
        """Click on forgot password link"""
        try:
            self.click_element(self.FORGOT_PASSWORD_LINK)
            self.logger.info("Clicked on forgot password link")
        except Exception as e:
            self.logger.error(f"Failed to click forgot password link: {str(e)}")
            raise e

    def is_login_page_displayed(self):
        """Check if login page is displayed"""
        try:
            return (self.is_element_visible(self.LOGIN_BUTTON) and 
                   self.is_element_visible(self.EMAIL_INPUT) and 
                   self.is_element_visible(self.PASSWORD_INPUT))
        except Exception as e:
            self.logger.error(f"Failed to check if login page is displayed: {str(e)}")
            return False

    def is_dashboard_displayed(self):
        """Check if dashboard is displayed after successful login"""
        try:
            return (self.is_element_visible(self.DASHBOARD_HEADER) and 
                   self.is_element_visible(self.USER_MENU))
        except Exception as e:
            self.logger.error(f"Failed to check if dashboard is displayed: {str(e)}")
            return False

    def is_forgot_password_page_displayed(self):
        """Check if forgot password page is displayed"""
        try:
            return self.is_element_visible(self.FORGOT_PASSWORD_FORM)
        except Exception as e:
            self.logger.error(f"Failed to check if forgot password page is displayed: {str(e)}")
            return False

    def get_email_label_text(self):
        """Get email input label text"""
        try:
            return self.get_text(self.EMAIL_LABEL)
        except Exception as e:
            self.logger.error(f"Failed to get email label text: {str(e)}")
            return None

    def get_password_label_text(self):
        """Get password input label text"""
        try:
            return self.get_text(self.PASSWORD_LABEL)
        except Exception as e:
            self.logger.error(f"Failed to get password label text: {str(e)}")
            return None

    def is_remember_me_checked(self):
        """Check if remember me checkbox is checked"""
        try:
            return self.find_element(self.REMEMBER_ME_CHECKBOX).is_selected()
        except Exception as e:
            self.logger.error(f"Failed to check remember me status: {str(e)}")
            return False

    def logout(self):
        """Logout from the application"""
        try:
            self.click_element(self.USER_MENU)
            self.click_element(self.LOGOUT_BUTTON)
            self.logger.info("Logged out successfully")
        except Exception as e:
            self.logger.error(f"Failed to logout: {str(e)}")
            raise e

    def is_logged_out(self):
        """Check if user is logged out"""
        try:
            return self.is_login_page_displayed()
        except Exception as e:
            self.logger.error(f"Failed to check logout status: {str(e)}")
            return False 