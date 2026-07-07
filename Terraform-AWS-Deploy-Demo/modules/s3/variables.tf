variable "environment" {
  type = string
}

variable "market_region" {
  type = string
  description = "Multi-tenancy, environment isolation"
}

variable "force_destroy" {
  type    = bool
}




