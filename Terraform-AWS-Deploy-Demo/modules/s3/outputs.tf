output "s3_id" {
  description = "Name of bucket"
  value = aws_s3_bucket.applogs.id
}

output "s3_arn" {
  description = "ARN of bucket"
  value = aws_s3_bucket.applogs.arn
}

output "s3_domain" {
  description = "Bucket domain name"
  value = aws_s3_bucket.applogs.bucket_domain_name
}
