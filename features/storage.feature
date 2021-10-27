Feature: Test Storage Accounts
Scenario: Ensure storage accounts have the proper network rules
    Given I have Azure Storage Account defined
    Then it must contain network_rules
    Then its default_action must be "Allow"

Scenario: Ensure storage accounts use TLS 1.2 or above
    Given I have Azure Storage Account defined
    Then it must contain min_tls_version
    And its value must be TLS1_2

Scenario: Ensure storage accounts have purpose tags
    Given I have Azure Storage Account defined
    When it has tags
    Then it must contain purpose

