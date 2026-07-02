terraform {
  backend "s3" {
    bucket         = "terraform-aws-remote-tfstate-bucket20260702004645306300000001"
    key            = "environments/dev/terraform.tfstate"
    region         = "us-east-1"
    use_lockfile   = true
  }
}