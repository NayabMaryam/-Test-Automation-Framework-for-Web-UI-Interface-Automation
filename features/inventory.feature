
Feature: Inventory Management

  As a logged-in SauceDemo user
  I want to view and interact with products
  So that I can select products for purchase

  Background:
    Given the user is logged in to SauceDemo
    And the user is on the inventory page

  Scenario: Verify inventory page display
    Then the inventory page title should be "Products"
    And the inventory container should be visible

  Scenario: Verify all products are displayed
    Then 6 products should be displayed

  Scenario: Verify product names
    Then the following products should be displayed:
      | product_name                       |
      | Sauce Labs Backpack                |
      | Sauce Labs Bike Light              |
      | Sauce Labs Bolt T-Shirt             |
      | Sauce Labs Fleece Jacket            |
      | Sauce Labs Onesie                   |
      | Test.allTheThings() T-Shirt (Red)   |

  Scenario: Sort products by name ascending
    When the user sorts products by "Name (A to Z)"
    Then products should be sorted alphabetically

  Scenario: Sort products by price ascending
    When the user sorts products by "Price (low to high)"
    Then products should be sorted by price in ascending order
