variable "subscription_id" {
  type        = string
  description = "Subscription ID for azurerm resource provider"
}

variable "static_web_storage_account_name" {
  type        = string
  description = "The storage account name for hosting static web content"
}

variable "resource_group_name" {
  type        = string
  description = "The resource group name that will contain all of the cohort's resources"
}