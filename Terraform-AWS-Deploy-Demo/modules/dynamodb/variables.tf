variable "environment" {
  type = string
  default = "dev"
}

variable "market_region" {
  type = string
  description = "Multi-tenancy, environment isolation"
}

variable "billing_mode" {
  type = string
  description = "Used to set the billing mode"
}