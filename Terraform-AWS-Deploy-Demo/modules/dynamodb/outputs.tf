output "table_id" {
  description = "Name of table"
  value = aws_dynamo_table.log_index.id
}

output "table_arn" {
  description = "ARN of table"
  value = aws_dynamo_table.log_index.arn
}

