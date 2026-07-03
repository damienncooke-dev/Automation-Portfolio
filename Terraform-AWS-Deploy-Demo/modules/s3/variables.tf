variable "environment" {
  type = string
  default = "dev"
}

variable "market_namespace" {
  type = string
  description = "Multi-tenancy, environment isolation"
}