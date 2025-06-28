# BehaveAPI - API Automation Testing Framework

An API automation testing framework based on Python Behave, supporting REST API and WebSocket interface testing.

## Project Overview

BehaveAPI is a BDD (Behavior Driven Development) testing framework based on Python and Behave, supporting automated testing for REST APIs and WebSockets.

## Project Structure

```
behaveAPI/
├── features/                    # Feature files directory
│   ├── rest/                   # REST API test cases
│   │   └── candlestick.feature # Candlestick data interface tests
│   └── websocket/              # WebSocket test cases
├── features/steps/             # Step definitions directory
│   ├── rest_steps.py          # REST API step definitions
│   ├── ws_steps.py            # WebSocket step definitions
│   └── common_steps.py        # Common step definitions
├── features/environment.py     # Behave environment configuration
├── config/                     # Configuration files directory
│   ├── config.yml             # Main configuration file
│   └── .env.example           # Environment variables example
├── test_data/                  # Test data directory
│   └── test_data.json         # Test data file
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── assertions.py          # Assertion utilities
│   ├── logger.py              # Logging utilities
│   └── config_manager.py      # Configuration management
├── reports/                    # Test reports directory
├── requirements.txt            # Dependencies list
├── .env                        # Environment variables file (create manually)
├── .gitignore                 # Git ignore file
└── README.md                   # Project documentation
```

## Technology Stack

- **Python 3.8+**
- **Behave**: BDD testing framework
- **Requests**: REST API request library
- **websocket-client**: WebSocket client library
- **PyYAML**: YAML configuration file parsing
- **python-dotenv**: Environment variable management
- **jsonschema**: JSON Schema validation

## Installation Instructions

1. Clone the project

```bash
git clone <repository_url>
cd behaveAPI
```

2. Create virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables

```bash
cp config/.env.example .env
# Edit the .env file and set necessary environment variables
```

## Configuration

### Environment Variables (.env)

```
BASE_URL=https://uat-api.3ona.co
TIMEOUT=30
LOG_LEVEL=INFO
```

### Configuration File (config/config.yml)

```yaml
api:
  base_url: ${BASE_URL}
  timeout: ${TIMEOUT}
  headers:
    Content-Type: application/json

logging:
  level: ${LOG_LEVEL}
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## Test Case Design

### REST API Testing

#### Scenario 1: Valid Parameter Request

- Send GET request with all required parameters
- Verify response status code is 200
- Verify response body contains result.data
- Verify data contains fields like o, h, l, c

#### Scenario 2: Invalid Parameter Request

- Send request missing required parameters
- Verify error status code is returned
- Verify error response structure

## Execution Methods

### Run All Tests

```bash
behave
```

### Run Specific Feature Tests

```bash
# Run only REST API tests
behave features/rest/

# Run only WebSocket tests
behave features/websocket/
```

### Run Tests with Specific Tags

```bash
# Run tests tagged with @smoke
behave --tags=@smoke

# Run tests tagged with @rest
behave --tags=@rest
```

## Logging

Log files will be saved in the `reports/` directory, including:

- Request details (URL, Headers, Body)
- Response details (Status Code, Headers, Body)
- Assertion results
- Error information

## Extension Guide

### Adding New Test Cases

1. Create `.feature` files in the corresponding `features/` directory
2. Implement corresponding step definitions in `features/steps/`
3. Add test data in `test_data/` if needed

### Adding New Assertion Methods

Add custom assertion methods in `utils/assertions.py`

### Adding New Configuration Items

1. Add environment variables in `.env`
2. Reference environment variables in `config/config.yml`
3. Access configuration through `config_manager` in code

## Common Issues

### Q: How to switch test environments?

A: Modify the `BASE_URL` variable in the `.env` file

### Q: How to debug failed tests?

A:

1. Check log files in the `reports/` directory
2. Use `behave --no-capture` to view real-time output
3. Add breakpoints in step definitions for debugging

### Q: How to add new request headers?

A: Add them in the `headers` section of `config/config.yml`, or set them dynamically in step definitions

## Contributing Guidelines

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
