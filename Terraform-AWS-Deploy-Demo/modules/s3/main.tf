resource "aws_s3_bucket" "app_logs" {
  bucket = "demo-${var.environment}-${var.market_region}-logs"
  force_destroy = var.delete_data
}

# DevSecOps Best Practice: Ensure the state bucket is fully encrypted
resource "aws_s3_bucket_server_side_encryption_configuration" "prod_data_crypto" {
  bucket = aws_s3_bucket.app_logs.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# DevSecOps Best Practice: Block all public access to your state file
resource "aws_s3_bucket_public_access_block" "prod_data_privacy" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
