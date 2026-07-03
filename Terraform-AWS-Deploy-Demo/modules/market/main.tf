module "s3" {
  source           = "../s3"
  environment      = var.environment
  market_namespace = var.market_namespace
}

module "dynamodb" {
  source           = "../dynamodb"
  environment      = var.environment
  market_namespace = var.market_namespace
  billing_mode     = var.billing_mode
}

module "iam" {
  source           = "../iam"
  environment      = var.environment
  market_namespace = var.market_namespace
  bucket_arn       = module.s3.bucket_arn      # this variable must appear in iam/variables.tf. you will get "unsupported argument" if the module doesn't expect this input.
  table_arn        = module.dynamodb.table_arn #  ^(same)^
  trusted_role_arn = var.trusted_role_arn      #  ^(same)^
}
