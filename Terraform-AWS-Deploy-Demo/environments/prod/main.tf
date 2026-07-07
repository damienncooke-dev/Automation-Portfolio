
module "market_stack" {
  source           = "../../modules/market"
  for_each         = toset(var.market_region) # for_each only accepts map and set types, raw list types generate an error
  market_region    = each.value
  environment      = var.environment
  trusted_role_arn = var.trusted_role_arn
  billing_mode     = var.billing_mode
  ami_id           = var.ami_id
  force_destroy    = var.force_destroy
}
