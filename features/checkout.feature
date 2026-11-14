Feature: Checkout Management

  As a logged-in SauceDemo user
  I want to complete the checkout process
  So that I can purchase selected products


  Background:
    Given the user is logged in to SauceDemo
    And the user is on the inventory page


  Scenario: Verify checkout information page
    Given the user has added "Sauce Labs Bike Light" to the cart
    Then the checkout information page should be displayed


  Scenario: Verify checkout information validation
    Given the user has added "Sauce Labs Bike Light" to the cart
    When the user continues checkout without entering information
    Then the checkout error message should be "Error: First Name is required"


  Scenario: Enter valid checkout information
    Given the user has added "Sauce Labs Bike Light" to the cart
    When the user enters checkout information:
      | first_name | last_name | postal_code |
      | Tooba      | Nadeem    | 38000       |
    Then the checkout overview page should be displayed


  Scenario: Verify checkout overview details
    Given the user has added "Sauce Labs Bike Light" to the cart
    And the user has entered valid checkout information
    Then 1 product should be displayed in the checkout overview
    And the checkout product should be "Sauce Labs Bike Light"
    And the checkout item total should be 9.99
    And the checkout tax should be 0.80
    And the checkout total should be 10.79


  Scenario: Complete checkout successfully
    Given the user has added "Sauce Labs Bike Light" to the cart
    And the user has entered valid checkout information
    When the user finishes checkout
    Then the checkout confirmation page should be displayed
    And the order confirmation message should contain "Your order has been dispatched"


  Scenario: Complete checkout with an empty cart
    Given the user has an empty cart
    When the user enters checkout information:
      | first_name | last_name | postal_code |
      | Tooba      | Nadeem    | 38000       |
    Then the checkout overview should contain 0 products
    When the user finishes checkout
    Then the checkout confirmation page should be displayed