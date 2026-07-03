variable "environment" {
  type    = string
  default = "dev"
}

variable "market_namespace" {
  description = "Multi-tenancy, environment isolation"
  type        = string
  default     = "market-a"
}

variable "trusted_role_arn" {
  type = string
  description = "Used to grant the user permission to assume role"
}