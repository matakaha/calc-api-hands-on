terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.80.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-terraformsample"
    storage_account_name = "stmatakahaterra"
    container_name       = "terra001"
    key                  = "calcapi.tfstate"
    use_azuread_auth     = true
  }
}

provider "azurerm" {
  features {}
  storage_use_azuread = true
}
