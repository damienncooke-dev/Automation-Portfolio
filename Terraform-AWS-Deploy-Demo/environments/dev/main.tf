
module "market_stack" {
  source           = "../../modules/market"
  for_each         = toset(var.market_region) # for_each only accepts map and set types, raw list types generate an error.
  market_region    = each.value   # Values are {market-a, market-b, market-c}
  environment      = var.environment  # self = prod
  trusted_role_arn = var.trusted_role_arn   # Allows any IAM principle that has Assume Role enabled on their account to assume any of the market roles. 'trusted_role_arn' is picked up from ENV setting: 'TF_VAR_trusted_role_arn'
  billing_mode     = var.billing_mode   # Set to PAY-PER-USE
  ami_id           = var.ami_id   # Configured OS used to apply to EC2 instance.  Specific to aws_region
  force_destroy    = var.force_destroy  # Prevents accidental deletion of data when 'false', allows complete resource removal including data when 'true'
}
