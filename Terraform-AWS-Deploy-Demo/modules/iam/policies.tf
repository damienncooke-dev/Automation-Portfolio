# Trust Policy
data "aws_iam_policy_document" "instance_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

# Permission Policy
data "aws_iam_policy_document" "market_permissions" {
   # The 'statement' blocks below are the policy configurations for S3 and DynamoDB
   statement{
     sid = "S3ListBucket"
     actions = [
        "s3:ListBucket"
     ]
     resources = [
        var.bucket_arn
     ]
   }

   statement{
     sid = "S3Access"
     actions = [
        "s3:GetObject",
        "s3:PutObject"
     ]
     resources = [
        "${var.bucket_arn}/*"
     ]
   }

   statement{
     sid = "DynamodDBAccess"
     actions = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan"
     ]
     resources = [
        var.table_arn
     ]
   }
}
