# All custom roles and policies are created here
# Trust Policy
data "aws_iam_policy_document" "ec2_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
    principals {
      type        = "AWS"
      identifiers = [var.trusted_role_arn]
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
        var.bucket_arn    # only list permitted on the buckets with arn (e.g. arn:aws:s3:::demo-dev-market-a-logs)
     ]
   }

   statement{
     sid = "S3Access"
     actions = [
        "s3:GetObject",
        "s3:PutObject"
     ]
     resources = [
        "${var.bucket_arn}/*"   # actions allowed only on the objects in the bucket with arn (e.g. arn:aws:s3:::demo-dev-market-a-logs)
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
        var.table_arn   # actions allowed on tables with arn (e.g. arn:aws:dynamodb:us-east-1:...:table/demo-dev-market-a-log-index
     ]
   }
}

