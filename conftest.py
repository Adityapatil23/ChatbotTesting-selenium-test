import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import yaml
import os
import logging
from datetime import datetime

def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def setup_logging():
    """Setup logging configuration"""
    log_dir = os.path.join(os.path.dirname(__file__), 'reports', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

@pytest.fixture(scope="session")
def config():
    """Fixture to provide configuration"""
    return load_config()

@pytest.fixture(scope="session")
def logger():
    """Fixture to provide logger"""
    return setup_logging()

@pytest.fixture(scope="function")
def driver(config):
    """Fixture to provide WebDriver instance"""
    chrome_options = Options()
    if config['browser']['headless']:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        # Initialize Chrome driver with direct path
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(config['browser']['implicit_wait'])
        driver.maximize_window()
        
        yield driver
    except Exception as e:
        logging.error(f"Failed to initialize Chrome driver: {str(e)}")
        raise
    finally:
        try:
            if 'driver' in locals() and driver:
                driver.quit()
        except Exception as e:
            logging.error(f"Failed to quit Chrome driver: {str(e)}")

@pytest.fixture(scope="function")
def screenshot_on_failure(request, driver):
    """Fixture to take screenshot on test failure"""
    yield
    
    if request.node.rep_call.failed:
        screenshot_dir = os.path.join(os.path.dirname(__file__), 'reports', 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        
        screenshot_path = os.path.join(
            screenshot_dir,
            f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved: {screenshot_path}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
