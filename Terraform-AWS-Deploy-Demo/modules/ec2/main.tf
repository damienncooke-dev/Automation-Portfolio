resource "aws_instance" "app_server" {
  ami                    = var.ami_id
  instance_type          = "t3.micro"  # free tier resource
  iam_instance_profile   = var.iam_instance_profile

  tags = {
    Name        = "${var.environment}-app_server-${var.market_region}"
    Environment = var.environment
  }
}
