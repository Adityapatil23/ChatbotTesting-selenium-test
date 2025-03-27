<<<<<<< HEAD
# ChatbotTesting-selenium-test
=======
# Web Automation Framework with POM in Python

A robust web automation framework built with Python, Selenium, and Page Object Model (POM) design pattern.

## Features

- Python and PyTest for test automation
- Selenium WebDriver for web automation
- Allure Reports for beautiful test reporting
- Page Object Model (POM) and Page Factory implementation
- Element highlighting during test execution
- Parallel test execution with pytest-xdist
- MySQL database integration for data verification
- Screenshot capture on test failure
- Comprehensive logging
- Configuration management with YAML

## Prerequisites

- Python 3.8 or higher
- Chrome browser
- MySQL database
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
├── config.yaml              # Configuration file
├── conftest.py             # PyTest fixtures
├── requirements.txt        # Project dependencies
├── pages/                  # Page Object Model classes
│   ├── base_page.py
│   └── login_page.py
├── tests/                  # Test files
│   └── test_login_pom.py
├── utils/                  # Utility classes
│   └── db_utils.py
└── reports/               # Test reports and screenshots
    ├── allure-results/
    ├── logs/
    └── screenshots/
```

## Configuration

1. Update `config.yaml` with your settings:
```yaml
browser:
  name: chrome
  headless: false
  implicit_wait: 10
  explicit_wait: 20

urls:
  base_url: https://app.vwo.com
  login_url: https://app.vwo.com/#/login

database:
  host: localhost
  port: 3306
  database: test_db
  user: root
  password: root

test_data:
  valid_user:
    email: "test@example.com"
    password: "Test@123"
  invalid_user:
    email: "invalid@example.com"
    password: "Invalid@123"
```

## Running Tests

1. Run all tests:
```bash
pytest
```

2. Run tests in parallel:
```bash
pytest -n auto
```

3. Run specific test file:
```bash
pytest tests/test_login_pom.py
```

4. Run tests with specific marker:
```bash
pytest -m smoke
pytest -m regression
```

5. Generate Allure report:
```bash
allure serve reports/allure-results
```

## Test Reports

- HTML Report: `reports/report.html`
- Allure Report: `reports/allure-results`
- Screenshots: `reports/screenshots/`
- Logs: `reports/logs/`

## Database Setup

1. Create MySQL database:
```sql
CREATE DATABASE test_db;
```

2. Create users table:
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
>>>>>>> fef9b82 (Initial commit: ChatbotTesting selenium test)
