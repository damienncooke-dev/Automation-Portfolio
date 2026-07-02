output "aws_iam_role_id" {
  description = "Name of role"
  value = aws_iam_role.market_role.id
}

output "aws_iam_role_arn" {
  description = "ARN of role"
  value = aws_iam_role.market_role.arn
}


