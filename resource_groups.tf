resource "azurerm_resource_group" "edde_resource_group" {
  name     = var.resource_group_name
  location = "East US"
}