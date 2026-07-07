variable "environment" {
  type = string
}

variable "market_region" {
  type = string
  description = "Multi-tenancy, environment isolation"
}

variable "ami_id" {
  type = string
}

variable "iam_instance_profile" {
  type = string
}

