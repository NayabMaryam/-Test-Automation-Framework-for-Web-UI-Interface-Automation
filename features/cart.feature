
Feature: Shopping Cart Management

  As a logged-in SauceDemo user
  I want to manage products in my shopping cart
  So that I can review my selected products before checkout

  Background:
    Given the user is logged in to SauceDemo
    And the user is on the inventory page

  Scenario: Add a product to the cart
    When the user adds "Sauce Labs Backpack" to the cart
    Then the cart badge should display "1"

  Scenario: Add multiple products to the cart
    When the user adds "Sauce Labs Backpack" to the cart
    And the user adds "Sauce Labs Bike Light" to the cart
    Then the cart badge should display "2"

  Scenario: Verify products in the cart
    When the user adds "Sauce Labs Backpack" to the cart
    And the user adds "Sauce Labs Bike Light" to the cart
    And the user opens the shopping cart
    Then the cart page should be displayed
    And 2 products should be displayed in the cart

  Scenario: Remove a product from the cart
    When the user adds "Sauce Labs Backpack" to the cart
    And the user adds "Sauce Labs Bike Light" to the cart
    And the user opens the shopping cart
    And the user removes "Sauce Labs Backpack" from the cart
    Then 1 product should remain in the cart

  Scenario: Continue shopping from the cart
    When the user adds "Sauce Labs Backpack" to the cart
    And the user opens the shopping cart
    And the user continues shopping
    Then the inventory page should be displayed
