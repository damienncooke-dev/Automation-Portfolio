output "role_id" {
  description = "Name of role"
  value = aws_iam_role.market_role.id
}

output "role_arn" {
  description = "ARN of role"
  value = aws_iam_role.market_role.arn
}


