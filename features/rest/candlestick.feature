@candlestick
Feature: Candlestick API Testing
	As an API user
	I want to retrieve candlestick data
	So that I can analyze market trends

	Background:
		Given I have the API base URL configured
		And I set the request headers

	@smoke @positive
	Scenario: Get candlestick data with valid parameters
		Given I have valid candlestick parameters
		When I send a GET request to the candlestick endpoint
		Then the response status code should be 200
		And the response should contain "result.data"
		And the candlestick data should contain required fields
		And each candlestick should have "o" field
		And each candlestick should have "h" field
		And each candlestick should have "l" field
		And each candlestick should have "c" field

	@negative
	Scenario: Get candlestick data without instrument_name parameter
		Given I have candlestick parameters without instrument_name
		When I send a GET request to the candlestick endpoint
		Then the response status code should not be 200
		And the response should contain an error structure

	@negative
	Scenario: Get candlestick data with invalid instrument_name
		Given I have candlestick parameters with invalid instrument_name
		When I send a GET request to the candlestick endpoint
		Then the response status code should not be 200
		And the response should contain an error structure
