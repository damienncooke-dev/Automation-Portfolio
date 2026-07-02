output "bucket_id" {
  description = "Name of bucket"
  value = aws_s3_bucket.applogs.id
}

output "bucket_arn" {
  description = "ARN of bucket"
  value = aws_s3_bucket.applogs.arn
}

output "bucket_domain" {
  description = "Bucket domain name"
  value = aws_s3_bucket.applogs.bucket_domain_name
}
