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


resource "azurerm_service_plan" "func" {
  name                = "asp-${var.function_app_name}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name

  os_type  = "Linux"
  sku_name = "FC1"
}

resource "azurerm_linux_function_app" "func" {
  name                = var.function_app_name
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name

  service_plan_id            = azurerm_service_plan.func.id
  storage_account_name       = azurerm_storage_account.func.name
  storage_uses_managed_identity = true

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.func.id]
  }

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME           = "python"
    FUNCTIONS_EXTENSION_VERSION        = "~4"
    AzureWebJobsStorage__accountName   = azurerm_storage_account.func.name
    AzureWebJobsStorage__credential    = "managedidentity"
    AzureWebJobsStorage__clientId      = azurerm_user_assigned_identity.func.client_id
    WEBSITE_RUN_FROM_PACKAGE           = "1"
  }

}
