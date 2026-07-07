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

variable "billing_mode" {
  type    = string
}

# This ami_id is specific to "us-east-1/N.Virginia"
variable "ami_id" {
  type    = string
}

variable "force_destroy" {
  type    = bool
}


