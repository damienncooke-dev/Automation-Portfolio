variable "environment" {
  default = "prod"
}

variable "aws_region" {
  default = "us-west-1"
}

variable "market_region" {
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
  type    = string
  default = "PAY_PER_REQUEST"
}

# This ami_id is specific to "us-west-1/N.California"
variable "ami_id" {
  type    = string
  default = "ami-07fdf51168766b58a"
}

variable "force_destroy" {
  type    = bool
  default = true
}

