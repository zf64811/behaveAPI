@websocket @book
Feature: WebSocket Book Subscription Testing
    As an API user
    I want to subscribe to order book data via WebSocket
    So that I can receive real-time market depth information

    Background:
        Given I have the WebSocket URL configured
        And I set the WebSocket timeout

    @smoke @positive
    Scenario: Subscribe to order book with simple parameters
        Given I have a WebSocket connection to the book endpoint
        And I prepare a simple book subscription message
        When I send the subscription message
        Then I should receive a successful subscription response
        And the response should contain subscription confirmation
        And the book data should contain required fields with simple parameters
        And the trade data should contain required fields
        And each trade entry should have required fields


    @positive
    Scenario: Subscribe to order book with full parameters
        Given I have a WebSocket connection to the book endpoint
        And I prepare a full book subscription message
        When I send the subscription message
        Then I should receive a successful subscription response
        And the response should contain subscription confirmation
        And the book data should contain required fields
        And the book should have asks and bids arrays
        And each order entry should have price, size, and count

    @negative
    Scenario: Subscribe with invalid channel
        Given I have a WebSocket connection to the book endpoint
        And I prepare an invalid subscription message
        When I send the subscription message
        Then I should receive an error response
        And the error should indicate invalid channel