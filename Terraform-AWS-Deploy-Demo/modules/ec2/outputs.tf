output "ec2_app_server_id" {
  description = "Name of instance"
  value = aws_instance.app_server.id
}

output "ec2_app_server_arn" {
  description = "ARN of instance"
  value = aws_instance.app_server.arn
}
