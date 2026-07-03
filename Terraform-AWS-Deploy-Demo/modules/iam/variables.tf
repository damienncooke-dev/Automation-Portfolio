variable "environment" {
  type = string
  default = "dev"
}

variable "market_namespace" {
  description = "Multi-tenancy, environment isolation"
  type = string
  default = "market-a"
}

variable "bucket_arn" {
  type = string
  description = "The ARN of the bucket from the s3 module"
}

variable "table_arn" {
  type = string
  description = "The ARN of the table from the dynamodb module"
}

variable "trusted_role_arn" {
  type = string
  description = "Used to grant the user permission to assume role"
}