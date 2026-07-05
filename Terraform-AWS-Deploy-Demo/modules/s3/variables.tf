variable "environment" {
  type = string
  default = "dev"
}

variable "market_region" {
  type = string
  description = "Multi-tenancy, environment isolation"
}