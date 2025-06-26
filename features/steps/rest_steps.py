"""Step definitions for REST API testing."""

import json
import requests
from behave import given, when, then
from utils.logger import get_logger
from utils.assertions import assertions

logger = get_logger(__name__)


@given('I have the API base URL configured')
def step_have_base_url(context):
    """Verify base URL is configured."""
    assert context.base_url is not None, "Base URL is not configured"
    logger.info(f"Using base URL: {context.base_url}")


@given('I set the request headers')
def step_set_headers(context):
    """Set request headers from configuration."""
    context.request_headers = context.headers.copy()
    logger.debug(f"Request headers: {context.request_headers}")


@given('I add "{header_name}" header with value "{header_value}"')
def step_add_header(context, header_name, header_value):
    """Add a specific header to the request."""
    if not hasattr(context, 'request_headers'):
        context.request_headers = {}
    context.request_headers[header_name] = header_value
    logger.debug(f"Added header: {header_name} = {header_value}")


@given('I have valid candlestick parameters')
def step_valid_candlestick_params(context):
    """Set valid candlestick parameters."""
    # Load test data
    print("✅ LOADED: rest_steps.py")
    with open('test_data/test_data.json', 'r') as f:
        test_data = json.load(f)

    context.request_params = test_data['candlestick']['valid_params']
    logger.debug(f"Request parameters: {context.request_params}")


@given('I have candlestick parameters without instrument_name')
def step_candlestick_params_without_instrument(context):
    """Set candlestick parameters without instrument_name."""
    with open('test_data/test_data.json', 'r') as f:
        test_data = json.load(f)

    context.request_params = test_data['candlestick']['invalid_params'][
        'missing_instrument']
    logger.debug(
        f"Request parameters (missing instrument): {context.request_params}")


@given('I have candlestick parameters with invalid instrument_name')
def step_candlestick_params_invalid_instrument(context):
    """Set candlestick parameters with invalid instrument_name."""
    with open('test_data/test_data.json', 'r') as f:
        test_data = json.load(f)

    context.request_params = test_data['candlestick']['invalid_params'][
        'invalid_instrument']
    logger.debug(
        f"Request parameters (invalid instrument): {context.request_params}")


@when('I send a GET request to the candlestick endpoint')
def step_send_get_candlestick(context):
    """Send GET request to candlestick endpoint."""
    print("✅ LOADED: rest_steps.py")
    endpoint = context.api_config['endpoints']['candlestick']
    url = f"{context.base_url}{endpoint}"

    logger.log_request(method="GET",
                       url=url,
                       headers=context.request_headers,
                       params=context.request_params)

    try:
        context.response = requests.get(url,
                                        headers=context.request_headers,
                                        params=context.request_params,
                                        timeout=context.timeout)

        # Log response
        logger.log_response(
            status_code=context.response.status_code,
            headers=dict(context.response.headers),
            body=context.response.text[:500]
            if context.response.text else None,
            elapsed_time=context.response.elapsed.total_seconds())

        # Try to parse JSON response
        try:
            context.response_json = context.response.json()
        except json.JSONDecodeError:
            context.response_json = None
            logger.warning("Response is not valid JSON")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise


@when('I send a {method} request to "{endpoint}"')
def step_send_request(context, method, endpoint):
    """Send HTTP request to specified endpoint."""
    url = f"{context.base_url}{endpoint}"

    # Get request data from context
    headers = getattr(context, 'request_headers', {})
    params = getattr(context, 'request_params', None)
    data = getattr(context, 'request_body', None)

    logger.log_request(method=method,
                       url=url,
                       headers=headers,
                       params=params,
                       body=data)

    try:
        context.response = requests.request(method=method,
                                            url=url,
                                            headers=headers,
                                            params=params,
                                            json=data,
                                            timeout=context.timeout)

        logger.log_response(
            status_code=context.response.status_code,
            headers=dict(context.response.headers),
            body=context.response.text[:500]
            if context.response.text else None,
            elapsed_time=context.response.elapsed.total_seconds())

        # Try to parse JSON response
        try:
            context.response_json = context.response.json()
        except json.JSONDecodeError:
            context.response_json = None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise


@then('the response status code should be {expected_code:d}')
def step_check_status_code(context, expected_code):
    """Check response status code."""
    print("✅ LOADED: rest_steps.py")
    assertions.assert_status_code(context.response, expected_code)


@then('the response status code should not be {expected_code:d}')
def step_check_status_code_not(context, expected_code):
    """Check response status code is not the expected value."""
    actual_code = context.response.status_code
    assertions.assert_not_equals(
        actual_code, expected_code,
        f"Expected status code to not be {expected_code}, but it was")


@then('the response should contain "{key_path}"')
def step_response_contains_key(context, key_path):
    """Check if response contains a specific key."""
    assert context.response_json is not None, "Response is not valid JSON"
    assertions.assert_json_contains(context.response_json, key_path)


@then('the response should not contain "{key_path}"')
def step_response_not_contains_key(context, key_path):
    """Check if response does not contain a specific key."""
    assert context.response_json is not None, "Response is not valid JSON"
    assertions.assert_json_not_contains(context.response_json, key_path)


@then('the response "{key_path}" should equal "{expected_value}"')
def step_response_key_equals(context, key_path, expected_value):
    """Check if response key has expected value."""
    assert context.response_json is not None, "Response is not valid JSON"

    # Convert expected value to appropriate type
    if expected_value.lower() == 'true':
        expected_value = True
    elif expected_value.lower() == 'false':
        expected_value = False
    elif expected_value.isdigit():
        expected_value = int(expected_value)

    assertions.assert_json_contains(context.response_json, key_path,
                                    expected_value)


@then('the response should contain an error structure')
def step_response_contains_error(context):
    """Check if response contains an error structure."""
    assert context.response_json is not None, "Response is not valid JSON"

    # Check for common error fields
    has_error = False
    error_fields = ['error', 'message', 'code', 'error_message', 'error_code']

    for field in error_fields:
        try:
            if field in context.response_json:
                has_error = True
                logger.debug(f"Found error field: {field}")
                break
        except:
            pass

    assert has_error, "Response does not contain an error structure"


@then('the candlestick data should contain required fields')
def step_candlestick_has_required_fields(context):
    """Check if candlestick data contains all required fields."""
    assert context.response_json is not None, "Response is not valid JSON"

    # Get the data array
    data = context.response_json.get('result', {}).get('data', [])
    assertions.assert_list_not_empty(data)

    # Load expected fields from test data
    with open('test_data/test_data.json', 'r') as f:
        test_data = json.load(f)
    expected_fields = test_data['candlestick']['expected_fields']

    # Check first candlestick has all required fields
    if data:
        first_candle = data[0]
        for field in expected_fields:
            assert field in first_candle, f"Candlestick missing required field: {field}"
        logger.debug(f"All required fields present: {expected_fields}")


@then('each candlestick should have "{field}" field')
def step_each_candlestick_has_field(context, field):
    """Check if each candlestick has a specific field."""
    assert context.response_json is not None, "Response is not valid JSON"

    data = context.response_json.get('result', {}).get('data', [])
    assertions.assert_list_not_empty(data)

    for i, candle in enumerate(data):
        assert field in candle, f"Candlestick at index {i} missing field: {field}"

    logger.debug(f"All {len(data)} candlesticks have field: {field}")


@then('the response time should be less than {max_seconds:f} seconds')
def step_check_response_time(context, max_seconds):
    """Check if response time is within acceptable limit."""
    elapsed_time = context.response.elapsed.total_seconds()
    assertions.assert_response_time(elapsed_time, max_seconds)
