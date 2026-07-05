# The 'resource' below creates the Trust policy required by AWS when combined with policies.tf: "data.aws_iam_policy_document.instance_assume_role_policy.json"
resource "aws_iam_role" "market_role" {
  name               = "demo-${var.environment}-${var.market_region}-role"
  path               = "/market/"
  assume_role_policy = data.aws_iam_policy_document.instance_assume_role_policy.json
}

# The 'resource' below creates the Permission policy when combined with policies.tf: "data.aws_iam_policy_document.market_permissions.json"
resource "aws_iam_policy" "market_policy"{
  name        = "demo-${var.environment}-${var.market_region}-policy"
  description = "Tenant scoped policy"
  policy = data.aws_iam_policy_document.market_permissions.json
}

# Here we attach the permission policy resource: "market_policy" to the role: "market_role" and give it it's permission boundaries
resource "aws_iam_role_policy_attachment" "market_attach" {
  role       = aws_iam_role.market_role.name
  policy_arn = aws_iam_policy.market_policy.arn
}








