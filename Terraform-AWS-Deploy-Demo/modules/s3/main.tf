resource "aws_s3_bucket" "app_logs" {
  bucket = "demo-${var.environment}-${var.market_namespace}-logs"
}
