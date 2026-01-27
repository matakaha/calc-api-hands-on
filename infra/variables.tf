variable "location" {
  type        = string
  description = "Azure region"
  default     = "japaneast"
}

variable "function_app_name" {
  type        = string
  description = "Function App name"
  default     = "calcapimatakaha"
}

variable "resource_group_name" {
  type        = string
  description = "Resource group name"
  default     = "rg-calc-api-matakaha"
}

variable "storage_account_name" {
  type        = string
  description = "Storage account name for Functions"
  default     = "stcalcapimatakaha"
}
