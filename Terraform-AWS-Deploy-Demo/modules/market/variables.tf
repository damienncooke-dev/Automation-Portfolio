variable "environment" {
  type    = string
  default = "dev"
}

variable "market_region" {
  type        = string
  description = "Multi-tenancy, environment isolation"
}

variable "trusted_role_arn" {
  type = string
  description = "Used to grant the user permission to assume role"
}