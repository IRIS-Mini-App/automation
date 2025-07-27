# IRIS Mini App Automation Testing

Automated testing framework for IRIS Mini App using Python, Appium, and Pytest. This framework provides a robust, maintainable, and scalable solution for automated testing of the IRIS Mini App.

## Quick Links
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Test Reports](#test-reports)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- **Python**: 3.13 or higher
- **Android Tools**:
  - Android SDK
  - Emulator or real device
- **Appium**:
  - Appium Server 2.0+
  - Node.js 18+
- **JDK**: Version 17+

## Setup

1. **Clone & Navigate**:
   ```bash
   git clone https://github.com/IRIS-Mini-App/automation.git
   cd automation
   ```

2. **Virtual Environment**:
   ```bash
   python -m venv .venv
   # For Linux/Mac:
   source .venv/bin/activate
   # For Windows:
   .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Appium**:
   ```bash
   npm install -g appium
   appium driver install uiautomator2
   ```

5. **Configure Environment**:
   - Prepare Android device/emulator
   - Copy `test_settings.example.py` to `test_settings.py`
   - Update settings as needed

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
├── conftest.py            # Pytest fixtures
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Python dependencies
└── test_settings.py       # Environment settings
```

## Running Tests

### Quick Start
```bash
pytest -v                     # Run all tests
pytest tests/test_e2e.py -v  # Run specific test
pytest -v -m smoke           # Run smoke tests
```

### Common Options
| Option | Description |
|--------|-------------|
| `-v` | Verbose output |
| `-s` | Show print statements |
| `-k "test_name"` | Run tests by name |
| `--reruns N` | Retry failed tests |
| `-n auto` | Parallel execution |

### Report Generation
```bash
# Generate & view Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

## Test Reports

### Allure Reports
- **Location**: `allure-results/` directory
- **Features**:
  - Detailed test execution steps
  - Screenshots and logs
  - Test history and trends
  - Search and filter capabilities

### Logs
- **Location**: `logs/` directory
- **Organization**:
  - Date-based folders
  - Session-specific files
  - Detailed Appium server logs

## Development

### Code Quality Standards
- ✓ PEP 8 style guide
- ✓ Pylint score: 10.00/10
- ✓ Pre-commit hooks

### Contributing Guidelines
1. Branch from master
2. Make focused changes
3. Verify tests & lint
4. Submit detailed PR

## Troubleshooting

### Common Issues

#### 1. Appium Connection
- ✓ Verify server status
- ✓ Check port availability
- ✓ Confirm device connection

#### 2. Environment Setup
- ✓ Python version check
- ✓ Dependencies verification
- ✓ SDK/device validation

#### 3. Report Generation
- ✓ Allure installation
- ✓ Directory permissions
- ✓ Storage space
