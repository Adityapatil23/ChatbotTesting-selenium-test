from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import yaml
import os
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.actions = ActionChains(self.driver)
        self.load_config()
        self.setup_logging()

    def load_config(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def setup_logging(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def find_element(self, locator, timeout=20):
        """Find element with explicit wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.highlight_element(element)
            return element
        except Exception as e:
            self.logger.error(f"Element not found: {locator}")
            raise e

    def find_elements(self, locator, timeout=20):
        """Find elements with explicit wait"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except Exception as e:
            self.logger.error(f"Elements not found: {locator}")
            raise e

    def click_element(self, locator, timeout=20):
        """Click element with explicit wait"""
        try:
            element = self.find_element(locator, timeout)
            element.click()
        except Exception as e:
            self.logger.error(f"Failed to click element: {locator}")
            raise e

    def send_keys(self, locator, text, timeout=20):
        """Send keys to element with explicit wait"""
        try:
            element = self.find_element(locator, timeout)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f"Failed to send keys to element: {locator}")
            raise e

    def get_text(self, locator, timeout=20):
        """Get text from element with explicit wait"""
        try:
            element = self.find_element(locator, timeout)
            return element.text
        except Exception as e:
            self.logger.error(f"Failed to get text from element: {locator}")
            raise e

    def highlight_element(self, element, duration=1):
        """Highlight element for visual feedback"""
        try:
            original_style = element.get_attribute('style')
            self.driver.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);",
                element,
                "background: yellow; border: 2px solid red;"
            )
            self.driver.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);",
                element,
                original_style
            )
        except Exception as e:
            self.logger.error("Failed to highlight element")
            raise e

    def is_element_visible(self, locator, timeout=20):
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False

    def is_element_present(self, locator, timeout=20):
        """Check if element is present in DOM"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except:
            return False 