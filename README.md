# IRIS Mini App Automation Testing

Automated testing framework for IRIS Mini App using Python, Appium, and Pytest. This framework provides a robust, maintainable, and scalable solution for automated testing of the IRIS Mini App.

## Prerequisites

- Python 3.13 or higher
- Android SDK and emulator/real device
- Appium Server 2.0 or higher
- Node.js 18+ (for Appium)
- Java Development Kit (JDK) 17+

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

4. Install Appium server:
```bash
npm install -g appium
```

5. Install Appium Android driver:
```bash
appium driver install uiautomator2
```

6. Set up Android emulator or connect a physical device

7. Configure test settings:
   - Copy `test_settings.example.py` to `test_settings.py`
   - Modify settings according to your environment

## Project Structure

```
automation/
├── apks/                   # Android APK files
├── config/                 # Configuration files
├── pages/                  # Page objects (POM pattern)
├── screens/                # Screen objects for mobile UI
├── tests/                  # Test cases and test data
├── utils/                  # Utility functions and helpers
│   ├── appium_launcher.py # Appium server management
│   ├── custom_keywords.py # Custom test keywords
│   ├── driver_factory.py  # WebDriver initialization
│   ├── logger.py         # Logging configuration
│   └── test_helpers.py   # Test helper functions
├── conftest.py            # Pytest fixtures and configuration
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Python dependencies
└── test_settings.py       # Test environment settings
```

## Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_e2e.py -v

# Run tests with specific marker
pytest -v -m smoke
```

### Test Options
- `-v`: Verbose output
- `-s`: Show print statements
- `-k "test_name"`: Run tests matching the given name
- `--reruns N`: Rerun failed tests N times
- `-n auto`: Run tests in parallel

### Generate Reports
```bash
# Generate Allure report
pytest --alluredir=allure-results

# View report in browser
allure serve allure-results
```

## Test Reports

- **Allure Reports**: Detailed test execution reports with screenshots, logs, and steps
  - Located in `allure-results/`
  - Includes test steps, attachments, and execution history
  - Supports filtering and searching test results

## Logs

- Test execution logs are stored in the `logs/` directory
- Logs are organized by date and test session
- Debug logs include detailed Appium server and test execution information

## Development

### Code Quality
- Code follows PEP 8 style guide
- Current Pylint score: 10.00/10
- Pre-commit hooks enforce code quality standards

### Contributing
1. Create a new branch from master
2. Make your changes
3. Ensure all tests pass and maintain code quality
4. Submit a pull request with clear description of changes

## Troubleshooting

Common issues and solutions:

1. **Appium Connection Issues**
   - Verify Appium server is running
   - Check port availability
   - Ensure device/emulator is connected

2. **Test Environment Issues**
   - Verify Python version and virtual environment
   - Check all dependencies are installed
   - Validate Android SDK and device setup

3. **Report Generation Issues**
   - Ensure Allure is installed correctly
   - Check write permissions for report directory

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
