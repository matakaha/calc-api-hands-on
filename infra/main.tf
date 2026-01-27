data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

resource "azurerm_user_assigned_identity" "func" {
  name                = "id-${var.function_app_name}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
}

resource "azurerm_storage_account" "func" {
  name                     = var.storage_account_name
  resource_group_name      = data.azurerm_resource_group.main.name
  location                 = data.azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"

  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = true
}

resource "azurerm_storage_container" "func" {
  name                  = "func-content"
  storage_account_id    = azurerm_storage_account.func.id
  container_access_type = "private"
}

resource "azurerm_role_assignment" "func_storage_blob_contributor" {
  scope                = azurerm_storage_account.func.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.func.principal_id
}


resource "azurerm_service_plan" "func" {
  name                = "asp-${var.function_app_name}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name

  os_type  = "Linux"
  sku_name = "FC1"
}

resource "azurerm_function_app_flex_consumption" "func" {
  name                = var.function_app_name
  resource_group_name = data.azurerm_resource_group.main.name
  location            = data.azurerm_resource_group.main.location

  service_plan_id = azurerm_service_plan.func.id

  storage_container_type      = "blobContainer"
  storage_container_endpoint  = "${azurerm_storage_account.func.primary_blob_endpoint}${azurerm_storage_container.func.name}"
  storage_authentication_type = "UserAssignedIdentity"
  storage_user_assigned_identity_id = azurerm_user_assigned_identity.func.id

  runtime_name    = "python"
  runtime_version = "3.11"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.func.id]
  }

  site_config {
  }

  app_settings = {
    AzureWebJobsStorage              = azurerm_storage_account.func.primary_connection_string
    DEPLOYMENT_STORAGE_CONNECTION_STRING = azurerm_storage_account.func.primary_connection_string
  }
}
