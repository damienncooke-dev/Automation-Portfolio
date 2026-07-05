variable "environment" {
  default = "dev"
}

variable "aws_region" {
  default = "us-east-1"
}

variable "market_region" {
  type    = list(string)
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
  default = "PAY_PER_REQUEST"
}