output "role_id" {
  description = "Name of role"
  value = aws_iam_role.market_role.id
}

output "role_arn" {
  description = "ARN of role"
  value = aws_iam_role.market_role.arn
}

output "market_instance" {
  description = "The instance profile to attach to ec2 instance"
  value = aws_iam_instance_profile.ec2_profile.name
}

output "instance_profile_name" {
  description = "The instance profile to attach to ec2 instance"
  value = aws_iam_instance_profile.ec2_profile.name
}
