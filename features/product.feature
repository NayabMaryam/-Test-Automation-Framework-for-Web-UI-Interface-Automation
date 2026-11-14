
Feature: Product Details Management

  As a logged-in SauceDemo user
  I want to view individual product details
  So that I can inspect and select products for purchase

  Background:
    Given the user is logged in to SauceDemo
    And the user is on the inventory page

  Scenario: View individual product details
    When the user opens product "Sauce Labs Bike Light"
    Then the product details page should be displayed
    And the product name should be "Sauce Labs Bike Light"
    And the product description should contain "Water-resistant with 3 lighting modes"
    And the product price should be 9.99

  Scenario: Add a product to cart from its details page
    When the user opens product "Sauce Labs Bike Light"
    And the user adds the product to the cart
    Then the product should be added to the cart
    And the cart badge should display "1"

  Scenario: Remove a product from cart from its details page
    When the user opens product "Sauce Labs Bike Light"
    And the user adds the product to the cart
    And the user removes the product from the cart
    Then the product should be removed from the cart
    And the cart should be empty