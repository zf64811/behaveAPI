"""Behave environment configuration."""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.logger import get_logger
from utils.config_manager import config

# Initialize logger
logger = get_logger(__name__)


def before_all(context):
    """Run before all tests."""
    logger.info("Starting test execution")

    # Load configuration
    context.config = config
    context.api_config = config.get_api_config()
    context.test_data = config.get_test_data()

    # Initialize shared resources
    context.base_url = context.api_config.get('base_url')
    context.headers = context.api_config.get('headers', {})
    context.timeout = int(context.api_config.get('timeout', 30))

    logger.info(f"Base URL: {context.base_url}")
    logger.info(f"Default timeout: {context.timeout}s")


def after_all(context):
    """Run after all tests."""
    logger.info("Test execution completed")


def before_feature(context, feature):
    """Run before each feature."""
    logger.info(f"Starting feature: {feature.name}")

    # Feature-specific setup
    if "rest" in feature.tags:
        context.feature_type = "rest"
    elif "websocket" in feature.tags:
        context.feature_type = "websocket"
    else:
        context.feature_type = "unknown"


def after_feature(context, feature):
    """Run after each feature."""
    logger.info(f"Completed feature: {feature.name}")


def before_scenario(context, scenario):
    """Run before each scenario."""
    logger.info(f"Starting scenario: {scenario.name}")

    # Reset scenario-specific data
    context.response = None
    context.response_json = None
    context.ws_connection = None
    context.ws_messages = []


def after_scenario(context, scenario):
    """Run after each scenario."""
    logger.info(
        f"Completed scenario: {scenario.name} - Status: {scenario.status}")

    # Cleanup WebSocket connections if any
    if hasattr(context, 'ws_connection') and context.ws_connection:
        try:
            context.ws_connection.close()
            logger.debug("Closed WebSocket connection")
        except Exception as e:
            logger.error(f"Error closing WebSocket connection: {e}")

    # Log scenario result
    if scenario.status == "failed":
        logger.error(f"Scenario failed: {scenario.name}")
        if hasattr(context, 'response') and context.response:
            logger.error(
                f"Last response status: {context.response.status_code}")
            logger.error(f"Last response body: {context.response.text}")


def before_step(context, step):
    """Run before each step."""
    logger.debug(f"Executing step: {step.name}")


def after_step(context, step):
    """Run after each step."""
    if step.status == "failed":
        logger.error(f"Step failed: {step.name}")
        if step.error_message:
            logger.error(f"Error: {step.error_message}")
