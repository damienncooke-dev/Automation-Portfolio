# The Single S3 Bucket for both State Storage AND Native Locking
resource "aws_s3_bucket" "terraform_state" {
  bucket_prefix = "terraform-aws-remote-tfstate-bucket"
  force_destroy = false   # added to prevent deletion of tfstate if bucket is destroyed
}

# DevSecOps Best Practice: Ensure the state bucket is fully encrypted
resource "aws_s3_bucket_server_side_encryption_configuration" "tfstate_crypto" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# DevSecOps Best Practice: Block all public access to your state file
resource "aws_s3_bucket_public_access_block" "tfstate_privacy" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable versioning
resource "aws_s3_bucket_versioning" "state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"     # keep all versions of tfstate
  }
}
