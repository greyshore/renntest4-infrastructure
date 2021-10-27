resource "azurerm_storage_account" "edde_static_website" {
  name                      = var.static_web_storage_account_name
  resource_group_name       = azurerm_resource_group.edde_resource_group.name
  location                  = azurerm_resource_group.edde_resource_group.location
  account_kind              = "StorageV2"
  account_tier              = "Standard"
  account_replication_type  = "LRS"
  min_tls_version           = "TLS1_2"
  enable_https_traffic_only = true
  allow_blob_public_access  = true
  network_rules {
    default_action = "Allow"
  }

  static_website {
    index_document     = "index.html"
    error_404_document = "404.html"
  }

  tags = {
    "purpose" = "storage-data-app"
    "product" = "EDDE"
  }
}

data "azurerm_storage_container" "static_web_container" {
  name                 = "$web"
  storage_account_name = azurerm_storage_account.edde_static_website.name
}

data "azurerm_storage_account_blob_container_sas" "static_web_container_sas" {
  connection_string = azurerm_storage_account.edde_static_website.primary_connection_string
  container_name    = data.azurerm_storage_container.static_web_container.name
  https_only        = true

  start  = "2021-10-20T00:00:00Z"
  expiry = "2022-04-20T00:00:00Z"

  permissions {
    read   = true
    add    = true
    create = true
    write  = true
    delete = true
    list   = true
  }

  cache_control       = "max-age=5"
}

output "static_web_container_sas_url_query_string" {
  sensitive = true
  value = data.azurerm_storage_account_blob_container_sas.static_web_container_sas.sas
}
