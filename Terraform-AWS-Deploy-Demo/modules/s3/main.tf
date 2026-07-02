resource "aws_s3_bucket" "applogs" {
  bucket = "demo-${var.environment}-${var.market_namespace}-logs"
}
