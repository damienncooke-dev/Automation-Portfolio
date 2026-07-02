variable "environment" {
  type = string
  default = "dev"
}

variable "market_namespace" {
  description = "Multi-tenancy, environment isolation"
  type = string
  default = "market-a"
}