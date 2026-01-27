output "function_app_default_hostname" {
  value       = azurerm_function_app_flex_consumption.func.default_hostname
  description = "Function App default hostname"
}

output "resource_group_name" {
  value       = data.azurerm_resource_group.main.name
  description = "Resource group name"
}
