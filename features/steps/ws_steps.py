"""Step definitions for WebSocket testing."""

import json
import time
import websocket
from behave import given, when, then
from utils.logger import get_logger
from utils.assertions import assertions

logger = get_logger(__name__)


class WebSocketClient:
    """WebSocket client wrapper for testing."""
    def __init__(self, url, timeout=30):
        self.url = url
        self.timeout = timeout
        self.ws = None
        self.messages = []
        self.connected = False

    def connect(self):
        """Establish WebSocket connection."""
        try:
            self.ws = websocket.create_connection(self.url,
                                                  timeout=self.timeout)
            self.connected = True
            logger.info(f"WebSocket connected to {self.url}")
            return True
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            return False

    def send_message(self, message):
        """Send message through WebSocket."""
        if not self.connected or not self.ws:
            raise Exception("WebSocket not connected")

        if isinstance(message, dict):
            message = json.dumps(message)

        logger.debug(f"Sending WebSocket message: {message}")
        self.ws.send(message)

    def receive_message(self, timeout=10):
        """Receive message from WebSocket with timeout."""
        if not self.connected or not self.ws:
            raise Exception("WebSocket not connected")

        self.ws.settimeout(timeout)
        try:
            message = self.ws.recv()
            logger.debug(f"Received WebSocket message: {message}")

            # Try to parse as JSON
            try:
                parsed_message = json.loads(message)
                self.messages.append(parsed_message)
                return parsed_message
            except json.JSONDecodeError:
                self.messages.append(message)
                return message

        except websocket.WebSocketTimeoutException:
            logger.warning("WebSocket receive timeout")
            return None
        except Exception as e:
            logger.error(f"WebSocket receive error: {e}")
            return None

    def close(self):
        """Close WebSocket connection."""
        if self.ws:
            try:
                self.ws.close()
                self.connected = False
                logger.info("WebSocket connection closed")
            except Exception as e:
                logger.error(f"Error closing WebSocket: {e}")


@given('I have the WebSocket URL configured')
def step_ws_url_configured(context):
    """Verify WebSocket URL is configured."""
    time.sleep(1)  # Ensure any previous setup is complete
    ws_config = context.config.get('websocket', {})
    context.ws_url = ws_config.get('url')
    context.ws_timeout = int(ws_config.get('timeout', 30))

    assert context.ws_url is not None, "WebSocket URL is not configured"
    logger.info(f"Using WebSocket URL: {context.ws_url}")


@given('I set the WebSocket timeout')
def step_set_ws_timeout(context):
    """Set WebSocket timeout."""
    logger.debug(f"WebSocket timeout set to {context.ws_timeout}s")


@given('I have a WebSocket connection to the book endpoint')
def step_ws_connection_book(context):
    """Establish WebSocket connection to book endpoint."""
    context.ws_client = WebSocketClient(context.ws_url, context.ws_timeout)
    success = context.ws_client.connect()
    assert success, "Failed to establish WebSocket connection"


@given('I prepare a simple book subscription message')
def step_prepare_simple_book_message(context):
    """Prepare simple book subscription message."""
    with open('test_data/test_data.json', 'r') as f:
        test_data = json.load(f)

    context.subscription_message = test_data['websocket'][
        'subscription_messages']['book_simple']
    logger.debug(
        f"Prepared simple book subscription: {context.subscription_message}")


@given('I prepare a full book subscription message')
def step_prepare_full_book_message(context):
    """Prepare full book subscription message with all parameters."""
    with open('test_data/test_data.json', 'r') as f:
        test_data = json.load(f)

    context.subscription_message = test_data['websocket'][
        'subscription_messages']['book_full']
    logger.debug(
        f"Prepared full book subscription: {context.subscription_message}")


@given('I prepare an invalid subscription message')
def step_prepare_invalid_message(context):
    """Prepare invalid subscription message."""
    context.subscription_message = {
        "id": 999,
        "method": "subscribe",
        "params": {
            "channels": ["invalid.channel.10"]
        }
    }
    logger.debug(
        f"Prepared invalid subscription: {context.subscription_message}")


@when('I send the subscription message')
def step_send_subscription_message(context):
    """Send subscription message through WebSocket."""
    context.ws_client.send_message(context.subscription_message)
    logger.info("Subscription message sent")


@then('I should receive a successful subscription response')
def step_receive_successful_response(context):
    """Receive and verify successful subscription response."""
    # Keep receiving messages until we get a subscription response
    max_attempts = 5
    response = None

    for i in range(max_attempts):
        response = context.ws_client.receive_message(timeout=10)
        assert response is not None, "No response received from WebSocket"

        # Check if this is a heartbeat message
        if isinstance(response,
                      dict) and response.get('method') == 'public/heartbeat':
            logger.debug(
                f"Received heartbeat message, continuing to wait for subscription response"
            )
            continue

        # Check if this is a subscription response
        if isinstance(response, dict) and 'result' in response:
            break

    assert response is not None, "No subscription response received after multiple attempts"
    assert 'result' in response, f"Response does not contain 'result' field: {response}"

    # Store response in context for further validation
    context.ws_response = response
    logger.info("Received WebSocket response")
    logger.debug(f"WebSocket response: {json.dumps(response, indent=2)}")


@then('I should receive an error response')
def step_receive_error_response(context):
    """Receive and verify error response."""
    response = context.ws_client.receive_message(timeout=10)
    assert response is not None, "No error response received from WebSocket"

    context.ws_response = response
    logger.info("Received WebSocket error response")


@then('the response should contain subscription confirmation')
def step_response_contains_confirmation(context):
    """Check if response contains subscription confirmation."""
    assert context.ws_response is not None, "No WebSocket response available"

    # Check for success indicators
    if isinstance(context.ws_response, dict):
        # Check for success code
        if 'code' in context.ws_response:
            assertions.assert_equals(context.ws_response['code'], 0,
                                     "Expected success code 0")

        # Check for method confirmation
        if 'method' in context.ws_response:
            assertions.assert_equals(context.ws_response['method'],
                                     'subscribe',
                                     "Expected subscribe method confirmation")

    logger.debug("Subscription confirmation verified")


@then('the book data should contain required fields')
def step_book_data_has_required_fields(context):
    """Check if book data contains all required fields."""
    assert context.ws_response is not None, "No WebSocket response available"
    assert isinstance(context.ws_response,
                      dict), "Response is not a dictionary"

    # Load expected fields from test data
    with open('test_data/test_data.json', 'r') as f:
        test_data = json.load(f)

    expected_fields = test_data['websocket']['expected_response_fields'][
        'book_data']

    # Check result object has required fields
    result = context.ws_response.get('result', {})
    for field in expected_fields:
        assert field in result, f"Book data missing required field: {field}"

    logger.debug(f"All required book data fields present: {expected_fields}")


@then('the book data should contain required fields with simple parameters')
def step_book_data_has_required_fields(context):
    """Check if book data contains all required fields."""
    assert context.ws_response is not None, "No WebSocket response available"
    assert isinstance(context.ws_response,
                      dict), "Response is not a dictionary"

    # Load expected fields from test data
    with open('test_data/test_data.json', 'r') as f:
        test_data = json.load(f)

    expected_fields = test_data['websocket']['expected_response_fields'][
        'trade_data']

    # Check result object has required fields
    result = context.ws_response.get('result', {})
    for field in expected_fields:
        assert field in result, f"Book data missing required field: {field}"

    logger.debug(f"All required book data fields present: {expected_fields}")


@then('the book should have asks and bids arrays')
def step_book_has_asks_and_bids(context):
    """Check if book data has asks and bids arrays."""
    assert context.ws_response is not None, "No WebSocket response available"

    result = context.ws_response.get('result', {})
    data = result.get('data', [])
    channel = result.get('channel', '')

    logger.debug(f"Received data for channel: {channel}")
    logger.debug(f"Data array length: {len(data)}")

    assertions.assert_list_not_empty(data)

    # Check first book entry has asks and bids
    if data:
        book_entry = data[0]
        logger.debug(f"First data entry keys: {list(book_entry.keys())}")
        logger.debug(f"First data entry: {json.dumps(book_entry, indent=2)}")

        # For book updates, asks and bids are inside 'update' object
        if 'update' in book_entry:
            update_data = book_entry['update']
            assert 'asks' in update_data, "Book update missing asks array"
            assert 'bids' in update_data, "Book update missing bids array"

            # Log the actual asks and bids content
            logger.debug(f"Asks array: {update_data['asks']}")
            logger.debug(f"Bids array: {update_data['bids']}")

            # Check arrays exist (they might be empty initially)
            assert isinstance(update_data['asks'],
                              list), "Asks should be a list"
            assert isinstance(update_data['bids'],
                              list), "Bids should be a list"

            logger.debug(
                f"Book has {len(update_data['asks'])} asks and {len(update_data['bids'])} bids"
            )
        else:
            # Fallback to direct asks/bids if no update object
            assert 'asks' in book_entry, "Book entry missing asks array"
            assert 'bids' in book_entry, "Book entry missing bids array"

            # Check arrays exist (they might be empty initially)
            assert isinstance(book_entry['asks'],
                              list), "Asks should be a list"
            assert isinstance(book_entry['bids'],
                              list), "Bids should be a list"

            logger.debug(
                f"Book has {len(book_entry['asks'])} asks and {len(book_entry['bids'])} bids"
            )


@then('each order entry should have price, size, and count')
def step_order_entries_have_required_fields(context):
    """Check if each order entry has required fields."""
    assert context.ws_response is not None, "No WebSocket response available"

    result = context.ws_response.get('result', {})
    data = result.get('data', [])

    if data:
        book_entry = data[0]

        # For book updates, asks and bids are inside 'update' object
        if 'update' in book_entry:
            update_data = book_entry['update']
            asks = update_data.get('asks', [])
            bids = update_data.get('bids', [])
        else:
            asks = book_entry.get('asks', [])
            bids = book_entry.get('bids', [])

        # Check asks
        for i, ask in enumerate(asks):
            assert len(
                ask
            ) >= 3, f"Ask entry {i} should have at least 3 elements: [price, size, count]"
            # Verify elements are numeric strings
            assert ask[0].replace('.', '').replace(
                '-', '').isdigit(), f"Ask price {ask[0]} is not numeric"
            assert ask[1].replace('.', '').replace(
                '-', '').isdigit(), f"Ask size {ask[1]} is not numeric"
            assert ask[2].isdigit(), f"Ask count {ask[2]} is not numeric"

        # Check bids
        for i, bid in enumerate(bids):
            assert len(
                bid
            ) >= 3, f"Bid entry {i} should have at least 3 elements: [price, size, count]"
            # Verify elements are numeric strings
            assert bid[0].replace('.', '').replace(
                '-', '').isdigit(), f"Bid price {bid[0]} is not numeric"
            assert bid[1].replace('.', '').replace(
                '-', '').isdigit(), f"Bid size {bid[1]} is not numeric"
            assert bid[2].isdigit(), f"Bid count {bid[2]} is not numeric"

        logger.debug(f"All order entries have required fields")


@then('the error should indicate invalid channel')
def step_error_indicates_invalid_channel(context):
    """Check if error response indicates invalid channel."""
    assert context.ws_response is not None, "No WebSocket error response available"

    # Check for error indicators
    if isinstance(context.ws_response, dict):
        # Check for error code (non-zero)
        if 'code' in context.ws_response:
            assertions.assert_not_equals(context.ws_response['code'], 0,
                                         "Expected error code (non-zero)")

        # Check for error message
        if 'message' in context.ws_response:
            error_msg = context.ws_response['message'].lower()
            assert any(
                keyword in error_msg
                for keyword in ['invalid', 'error', 'channel']
            ), f"Error message should indicate invalid channel: {error_msg}"

    logger.debug("Error response indicates invalid channel")


@then('the trade data should contain required fields')
def step_trade_data_has_required_fields(context):
    """Check if trade data contains all required fields."""
    assert context.ws_response is not None, "No WebSocket response available"
    assert isinstance(context.ws_response,
                      dict), "Response is not a dictionary"

    # Load expected fields from test data
    with open('test_data/test_data.json', 'r') as f:
        test_data = json.load(f)

    expected_fields = test_data['websocket']['expected_response_fields'][
        'trade_data']

    # Check result object has required fields
    result = context.ws_response.get('result', {})
    for field in expected_fields:
        assert field in result, f"Trade data missing required field: {field}"

    logger.debug(f"All required trade data fields present: {expected_fields}")


@then('each trade entry should have required fields')
def step_trade_entries_have_required_fields(context):
    """Check if each trade entry has required fields."""
    assert context.ws_response is not None, "No WebSocket response available"

    result = context.ws_response.get('result', {})
    data = result.get('data', [])

    # Load expected trade entry fields from test data
    with open('test_data/test_data.json', 'r') as f:
        test_data = json.load(f)

    expected_trade_fields = test_data['websocket']['expected_response_fields'][
        'trade_entry']

    # Check each trade entry has required fields
    for i, trade_entry in enumerate(data):
        logger.debug(
            f"Checking trade entry {i}: {json.dumps(trade_entry, indent=2)}")

        for field in expected_trade_fields:
            assert field in trade_entry, f"Trade entry {i} missing required field: {field}"

        # Additional validation for specific fields
        # Check 'd' field (trade ID) is a string
        assert isinstance(trade_entry['d'],
                          str), f"Trade entry {i} 'd' field should be string"

        # Check 't' field (timestamp) is numeric
        assert isinstance(
            trade_entry['t'],
            (int, float)), f"Trade entry {i} 't' field should be numeric"

        # Check 'p' field (price) is a string representing a number
        assert isinstance(trade_entry['p'],
                          str), f"Trade entry {i} 'p' field should be string"
        assert trade_entry['p'].replace('.', '').replace('-', '').isdigit(
        ), f"Trade entry {i} 'p' field should be numeric string"

        # Check 'q' field (quantity) is a string representing a number
        assert isinstance(trade_entry['q'],
                          str), f"Trade entry {i} 'q' field should be string"
        assert trade_entry['q'].replace('.', '').replace('-', '').isdigit(
        ), f"Trade entry {i} 'q' field should be numeric string"

        # Check 's' field (side) is valid
        assert trade_entry['s'] in [
            'BUY', 'SELL'
        ], f"Trade entry {i} 's' field should be 'BUY' or 'SELL'"

        # Check 'i' field (instrument) is a string
        assert isinstance(trade_entry['i'],
                          str), f"Trade entry {i} 'i' field should be string"

        # Check 'm' field (maker order ID) is a string
        assert isinstance(trade_entry['m'],
                          str), f"Trade entry {i} 'm' field should be string"

    logger.debug(f"All {len(data)} trade entries have required fields")
