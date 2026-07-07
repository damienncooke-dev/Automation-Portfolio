module "s3" {
  source           = "../s3"
  environment      = var.environment
  market_region    = var.market_region
  force_destroy    = var.force_destroy
}

module "dynamodb" {
  source           = "../dynamodb"
  environment      = var.environment
  market_region    = var.market_region
  billing_mode     = var.billing_mode
}

module "ec2" {
  source           = "../ec2"
  environment      = var.environment
  market_region    = var.market_region
  ami_id           = var.ami_id   # comes directly from the root module in either dev or prod
  iam_instance_profile   = module.iam.instance_profile_name   # pulls the instance profile from the iam output "instance_profile"
}

module "iam" {
  source           = "../iam"
  environment      = var.environment
  market_region    = var.market_region
  bucket_arn       = module.s3.bucket_arn      # this variable must appear in iam/variables.tf. you will get "unsupported argument" if the module doesn't expect this input.
  table_arn        = module.dynamodb.table_arn #  ^(same)^
  trusted_role_arn = var.trusted_role_arn      #  ^(same)^
}
