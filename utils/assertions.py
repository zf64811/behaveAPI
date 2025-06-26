"""Custom assertion utilities for API testing."""

import json
from typing import Any, Dict, List, Optional, Union
from jsonschema import validate, ValidationError
from utils.logger import get_logger

logger = get_logger(__name__)


class AssertionError(Exception):
    """Custom assertion error with detailed message."""
    pass


class Assertions:
    """Custom assertions for API testing."""
    
    @staticmethod
    def assert_equals(actual: Any, expected: Any, message: str = None):
        """Assert that two values are equal.
        
        Args:
            actual: Actual value
            expected: Expected value
            message: Optional custom error message
            
        Raises:
            AssertionError: If values are not equal
        """
        if actual != expected:
            error_msg = message or f"Expected {expected}, but got {actual}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.debug(f"Assertion passed: {actual} == {expected}")
    
    @staticmethod
    def assert_not_equals(actual: Any, expected: Any, message: str = None):
        """Assert that two values are not equal.
        
        Args:
            actual: Actual value
            expected: Expected value
            message: Optional custom error message
            
        Raises:
            AssertionError: If values are equal
        """
        if actual == expected:
            error_msg = message or f"Expected values to be different, but both are {actual}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.debug(f"Assertion passed: {actual} != {expected}")
    
    @staticmethod
    def assert_status_code(response, expected_code: int):
        """Assert response status code.
        
        Args:
            response: Response object
            expected_code: Expected status code
            
        Raises:
            AssertionError: If status code doesn't match
        """
        actual_code = response.status_code
        if actual_code != expected_code:
            error_msg = f"Expected status code {expected_code}, but got {actual_code}"
            logger.error(error_msg)
            logger.error(f"Response body: {response.text}")
            raise AssertionError(error_msg)
        logger.debug(f"Status code assertion passed: {actual_code}")
    
    @staticmethod
    def assert_json_contains(json_data: Dict, key_path: str, expected_value: Any = None):
        """Assert that JSON contains a key and optionally check its value.
        
        Args:
            json_data: JSON data as dictionary
            key_path: Dot-separated path to the key (e.g., 'result.data')
            expected_value: Optional expected value
            
        Raises:
            AssertionError: If key not found or value doesn't match
        """
        keys = key_path.split('.')
        current_data = json_data
        
        for i, key in enumerate(keys):
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            else:
                path_so_far = '.'.join(keys[:i+1])
                error_msg = f"Key '{path_so_far}' not found in JSON"
                logger.error(error_msg)
                logger.error(f"Available keys: {list(current_data.keys()) if isinstance(current_data, dict) else 'Not a dict'}")
                raise AssertionError(error_msg)
        
        if expected_value is not None:
            if current_data != expected_value:
                error_msg = f"Expected '{key_path}' to be {expected_value}, but got {current_data}"
                logger.error(error_msg)
                raise AssertionError(error_msg)
        
        logger.debug(f"JSON contains assertion passed for key: {key_path}")
    
    @staticmethod
    def assert_json_not_contains(json_data: Dict, key_path: str):
        """Assert that JSON does not contain a key.
        
        Args:
            json_data: JSON data as dictionary
            key_path: Dot-separated path to the key
            
        Raises:
            AssertionError: If key is found
        """
        keys = key_path.split('.')
        current_data = json_data
        
        try:
            for key in keys:
                if isinstance(current_data, dict) and key in current_data:
                    current_data = current_data[key]
                else:
                    # Key not found, assertion passes
                    logger.debug(f"JSON not contains assertion passed: {key_path} not found")
                    return
            
            # If we reach here, key was found
            error_msg = f"Expected key '{key_path}' not to exist, but it was found with value: {current_data}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        except (KeyError, TypeError):
            # Key not found, assertion passes
            logger.debug(f"JSON not contains assertion passed: {key_path} not found")
    
    @staticmethod
    def assert_json_schema(json_data: Dict, schema: Dict):
        """Assert that JSON data matches a schema.
        
        Args:
            json_data: JSON data to validate
            schema: JSON schema
            
        Raises:
            AssertionError: If validation fails
        """
        try:
            validate(instance=json_data, schema=schema)
            logger.debug("JSON schema validation passed")
        except ValidationError as e:
            error_msg = f"JSON schema validation failed: {e.message}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_list_contains(lst: List, item: Any):
        """Assert that list contains an item.
        
        Args:
            lst: List to check
            item: Item to find
            
        Raises:
            AssertionError: If item not in list
        """
        if item not in lst:
            error_msg = f"Expected list to contain {item}, but it doesn't. List: {lst}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.debug(f"List contains assertion passed: {item} in list")
    
    @staticmethod
    def assert_list_not_empty(lst: List):
        """Assert that list is not empty.
        
        Args:
            lst: List to check
            
        Raises:
            AssertionError: If list is empty
        """
        if not lst:
            error_msg = "Expected list to be non-empty, but it's empty"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.debug(f"List not empty assertion passed: {len(lst)} items")
    
    @staticmethod
    def assert_greater_than(actual: Union[int, float], expected: Union[int, float]):
        """Assert that actual value is greater than expected.
        
        Args:
            actual: Actual value
            expected: Expected minimum value
            
        Raises:
            AssertionError: If actual is not greater than expected
        """
        if actual <= expected:
            error_msg = f"Expected {actual} to be greater than {expected}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.debug(f"Greater than assertion passed: {actual} > {expected}")
    
    @staticmethod
    def assert_less_than(actual: Union[int, float], expected: Union[int, float]):
        """Assert that actual value is less than expected.
        
        Args:
            actual: Actual value
            expected: Expected maximum value
            
        Raises:
            AssertionError: If actual is not less than expected
        """
        if actual >= expected:
            error_msg = f"Expected {actual} to be less than {expected}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.debug(f"Less than assertion passed: {actual} < {expected}")
    
    @staticmethod
    def assert_in_range(value: Union[int, float], min_val: Union[int, float], 
                       max_val: Union[int, float], inclusive: bool = True):
        """Assert that value is within a range.
        
        Args:
            value: Value to check
            min_val: Minimum value
            max_val: Maximum value
            inclusive: Whether range is inclusive
            
        Raises:
            AssertionError: If value is out of range
        """
        if inclusive:
            if value < min_val or value > max_val:
                error_msg = f"Expected {value} to be in range [{min_val}, {max_val}]"
                logger.error(error_msg)
                raise AssertionError(error_msg)
        else:
            if value <= min_val or value >= max_val:
                error_msg = f"Expected {value} to be in range ({min_val}, {max_val})"
                logger.error(error_msg)
                raise AssertionError(error_msg)
        logger.debug(f"In range assertion passed: {value} in range")
    
    @staticmethod
    def assert_response_time(elapsed_time: float, max_time: float):
        """Assert that response time is within acceptable limit.
        
        Args:
            elapsed_time: Actual response time in seconds
            max_time: Maximum acceptable time in seconds
            
        Raises:
            AssertionError: If response time exceeds limit
        """
        if elapsed_time > max_time:
            error_msg = f"Response time {elapsed_time:.2f}s exceeds maximum {max_time:.2f}s"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.debug(f"Response time assertion passed: {elapsed_time:.2f}s < {max_time:.2f}s")


# Create global instance for easy access
assertions = Assertions() 