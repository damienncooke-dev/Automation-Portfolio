module "s3" {
  source        = "../s3"
  environment   = var.environment
  market_region = var.market_region
  force_destroy = var.force_destroy
}

module "dynamodb" {
  source        = "../dynamodb"
  environment   = var.environment
  market_region = var.market_region
  billing_mode  = var.billing_mode
}

module "ec2" {
  source               = "../ec2"
  environment          = var.environment
  market_region        = var.market_region
  ami_id               = var.ami_id                       # Passed through from calling 'root' module. Specifies OS to be used in EC2
  iam_instance_profile = module.iam.instance_profile_name # Gets value from the 'output' of the iam module
}

module "iam" {
  source           = "../iam"
  environment      = var.environment
  market_region    = var.market_region
  bucket_arn       = module.s3.bucket_arn      # Gets value from the 'output' of the S3 module
  table_arn        = module.dynamodb.table_arn # Gets value from the 'output' of the dynamodb module
  trusted_role_arn = var.trusted_role_arn      # Passed through from calling 'root' module
}
