output "bucket_id" {
  description = "Name of bucket"
  value = aws_s3_bucket.app_logs.id
}

output "bucket_arn" {
  description = "ARN of bucket"
  value = aws_s3_bucket.app_logs.arn
}