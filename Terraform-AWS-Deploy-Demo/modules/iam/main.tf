# The 'resource' below creates the Trust policy to allow ec2 resource to assume the role "demo-${var.environment}-${var.market_region}-role"
resource "aws_iam_role" "market_role" {
  name               = "demo-${var.environment}-${var.market_region}-role"
  path               = "/market/"   # organize this role under "market"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role_policy.json
}

# The 'resource' below creates the Permission policy when combined with policies.tf: "data.aws_iam_policy_document.market_permissions.json"
resource "aws_iam_policy" "market_policy"{
  name        = "demo-${var.environment}-${var.market_region}-policy"
  description = "Tenant scoped policy"
  policy = data.aws_iam_policy_document.market_permissions.json
}

# Here we create an instance to attach the permission policy resource: "market_policy" to the role: "market_role" and give it it's permission boundaries
resource "aws_iam_role_policy_attachment" "market_instance" {
  role       = aws_iam_role.market_role.name
  policy_arn = aws_iam_policy.market_policy.arn
}

# The profile that will attach to the ec2 instance. The profile name is exposed on the output to be picked by the calling module and then passed to the ec2 resource.
resource "aws_iam_instance_profile" "ec2_profile" {
  name       = "demo-${var.environment}-${var.market_region}-ec2-profile"
  role       = aws_iam_role.market_role.name
}

# Attach AWS managed policy: "AmazonSSMManagedInstanceCore" to allow ssh to EC2 instances
resource "aws_iam_role_policy_attachment" "ssm_managed_policy" {
  role       = aws_iam_role.market_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}






