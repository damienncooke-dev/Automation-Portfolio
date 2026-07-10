variable "environment" {
  default = "dev"
}

variable "aws_region" {
  default = "us-east-1"
}

variable "market_region" {
  type = list(string)
  default = [
    "market-a",
    "market-b",
    "market-c"
  ]
}

# Picked up in ENV setting: 'TF_VAR_trusted_role_arn'
variable "trusted_role_arn" {
  type        = string
  description = "Used to grant the user permission to assume role"
}

variable "billing_mode" {
  type    = string
  default = "PAY_PER_REQUEST"
}

# This ami_id is specific to "us-east-1/N.Virginia"
variable "ami_id" {
  type    = string
  default = "ami-06067086cf86c58e6"
}

variable "force_destroy" {
  type    = bool
  default = true
}

