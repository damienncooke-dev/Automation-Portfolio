output "dynamo_id" {
  description = "Name of table"
  value = aws_dynamo_table.log_index.id
}

output "dynamo_arn" {
  description = "ARN of table"
  value = aws_dynamo_table.log_index.arn
}

