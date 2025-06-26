"""Common step definitions for all features."""

from behave import given, when, then
from utils.logger import get_logger

logger = get_logger(__name__)


@given('I wait for {seconds:d} seconds')
def step_wait(context, seconds):
    """Wait for specified number of seconds."""
    import time
    logger.debug(f"Waiting for {seconds} seconds")
    time.sleep(seconds)


@given('I set the timeout to {seconds:d} seconds')
def step_set_timeout(context, seconds):
    """Set request timeout."""
    context.timeout = seconds
    logger.debug(f"Timeout set to {seconds} seconds")


@then('I print the response')
def step_print_response(context):
    """Print the response for debugging."""
    if hasattr(context, 'response'):
        logger.info(f"Response Status: {context.response.status_code}")
        logger.info(f"Response Headers: {dict(context.response.headers)}")
        logger.info(f"Response Body: {context.response.text}")
    else:
        logger.warning("No response available to print")


@then('I save the response to context as "{key}"')
def step_save_response_to_context(context, key):
    """Save response or response data to context."""
    if hasattr(context, 'response_json') and context.response_json:
        setattr(context, key, context.response_json)
        logger.debug(f"Saved response JSON to context.{key}")
    elif hasattr(context, 'response'):
        setattr(context, key, context.response.text)
        logger.debug(f"Saved response text to context.{key}")
    else:
        logger.warning(f"No response available to save to context.{key}")
