variable "environment" {
  default = "prod"
}

variable "aws_region" {
  default = "us-west-1"
}

variable "market_namespaces" {
  type = list(string)
  default = [
    "market-a",
    "market-b",
    "market-c"
  ]
}

variable "trusted_role_arn" {
  type        = string
  description = "Used to grant the user permission to assume role"
}

variable "billing_mode" {
  type        = string
  default = "PROVISIONED"
}
