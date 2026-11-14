
Feature: User Login

  As a SauceDemo user
  I want to log in to the application
  So that I can access the inventory page

  Scenario: Login with valid credentials
    Given the user is on the SauceDemo login page
    When the user logs in with username "standard_user" and password "secret_sauce"
    Then the inventory page should be displayed

  Scenario Outline: Login with invalid credentials
    Given the user is on the SauceDemo login page
    When the user logs in with username "<username>" and password "<password>"
    Then the login error message should contain "<error_message>"

    Examples:
      | username      | password     | error_message                            |
      | invalid_user  | secret_sauce | Username and password do not match       |
      | standard_user | wrong_password | Username and password do not match    |
      | EMPTY         | secret_sauce | Username is required                     |
      | standard_user | EMPTY        | Password is required                     |
      | locked_out_user | secret_sauce | Sorry, this user has been locked out    |
