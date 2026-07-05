resource "aws_dynamodb_table" "log_index" {
  # Required arguments: name, hash_key, attribute
  name =  "demo-${var.environment}-${var.market_region}-log-index"
  hash_key = "log_id"
  billing_mode = var.billing_mode
  attribute {
    name = "log_id"
    type = "S"
  }
}
