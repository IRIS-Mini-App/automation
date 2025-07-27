# IRIS Mini App Automation Testing

Automated testing framework for IRIS Mini App using Python, Appium, and Pytest.

## Prerequisites

- Python 3.10 or higher
- Android SDK and emulator/real device
- Appium Server
- Node.js (for Appium)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/IRIS-Mini-App/automation.git
cd automation
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Android emulator or connect a physical device

## Project Structure

```
automation/
├── apks/                   # Android APK files
├── config/                 # Configuration files
├── pages/                  # Page objects
├── tests/                  # Test cases
├── utils/                  # Utility functions
├── conftest.py            # Pytest fixtures
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Python dependencies
└── test_settings.py      # Test settings
```

## Running Tests

To run all tests:
```bash
pytest -v
```

To run specific test:
```bash
pytest tests/test_recipe_input.py -v
```

To generate Allure report:
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## Test Reports

Test reports are generated using Allure framework and can be found in the `allure-results` directory after test execution.

## Logs

Test execution logs are stored in the `logs` directory with timestamps for easy tracking.
