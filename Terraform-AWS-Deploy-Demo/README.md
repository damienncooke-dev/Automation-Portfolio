# Terraform AWS Infrastructure Automation — SRE Portfolio Project

> **Purpose:** Demonstrates Infrastructure-as-Code proficiency using Terraform on AWS, covering beginner-to-intermediate concepts aligned with SRE environment automation roles. This project provisions multi-environment AWS infrastructure with a focus on modularity, state management, security, and operational best practices.

---

## Project Overview

This project provisions a realistic, multi-environment AWS infrastructure (e.g. dev / staging / prod) using Terraform. It demonstrates core SRE competencies including IaC lifecycle management, remote state, modular design, IAM least-privilege, and observability — mapped directly to the skills expected in environment automation roles.

**Tech Stack: PHASE 1 ** Terraform · AWS (IAM, S3, PostgreSQL, EC2)**

**Tech Stack: PHASE 2 ** Terraform · AWS (VPC, CloudWatch) · GitHub Actions CI/CD**

---

## Repository Structure

```
terraform-aws-sre-demo/
├── README.md
├── modules/
│   ├── ## Stage 1 ##
│   ├── iam/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── providers.tf
│   ├── s3/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── providers.tf
│   ├── postgresql/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── providers.tf
│   ├── ec2/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── providers.tf
│   ├── ## Stage 2 ##
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── monitoring/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/           # Use this directory to provision environments using workspaces. 
│   ├── dev/                
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   ├── main.tf
│   │   ├── ... (For display only. Not used in this demo.)
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       └── backend.tf
└── .gitignore
```

---

## Stage 1 — Terraform Foundations & Remote State Bootstrap

**Concepts demonstrated:** provider configuration, backend setup, S3 state storage, S3 state locking, S3 versioning enabled.

### 1.1 Provider Configuration

- Configure the `aws` provider with region variable
- Pin provider version with `required_providers` block
- Use `terraform.required_version` constraint

### 1.2 S3 Backend for Remote State

Provision an S3 bucket to store Terraform state files remotely:

- Enable versioning on the state bucket (supports state rollback)
- Enable server-side encryption (SSE-S3 or SSE-KMS)
- Block all public access
- Enable access logging to a separate S3 bucket

```hcl
# bootstrap/main.tf — run once to create the backend infrastructure
resource "aws_s3_bucket" "tf_state" {
  bucket = "your-org-terraform-state"
  # ... versioning, encryption, public access block
}
```

### 1.3 Backend Configuration Per Environment

Configure each environment to use the shared S3 backend with a unique state key:

```hcl
# environments/dev/backend.tf
terraform {
  backend "s3" {
    bucket         = "your-org-terraform-state"
    key            = "environments/dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

**SRE relevance:** Remote state with locking mirrors how teams safely manage IaC across many tenant environments without state corruption.

---

## Stage 2 — IAM: Identity and Least-Privilege Access

**Concepts demonstrated:** IAM roles, policies, instance profiles, policy attachment, data sources, least-privilege design.

### 2.1 IAM Module Structure (`modules/iam/`)

- Accept `environment` and `app_name` as input variables
- Output role ARN and instance profile name for consumption by other modules

### 2.2 IAM Role for EC2 (Instance Profile)

- Create an IAM role with an EC2 trust policy
- Attach a custom policy granting only the permissions needed (e.g., read from a specific S3 bucket, write to a specific DynamoDB table)
- Create an instance profile to attach the role to EC2 instances

```hcl
resource "aws_iam_role" "app_role" {
  name               = "${var.app_name}-${var.environment}-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}
```

### 2.3 Custom IAM Policy (Least Privilege)

- Use `aws_iam_policy_document` data source to build policies in HCL (not JSON strings)
- Scope permissions to specific resource ARNs using `module.s3.bucket_arn` and `module.dynamodb.table_arn` output references

### 2.4 Demonstrate Cross-Module Reference

Show how the IAM module consumes outputs from the S3 and DynamoDB modules to scope permissions to exact resource ARNs — illustrating module composition.

### 2.5 (Stretch) IAM for CI/CD Pipeline

- Create a dedicated IAM user or role for GitHub Actions with scoped permissions
- Use OIDC federation to avoid long-lived access keys (GitHub Actions → AWS trust relationship)

**SRE relevance:** Demonstrates understanding of isolation and least-privilege — critical when managing many tenant environments where blast radius must be minimized.

---

## Stage 3 — S3: Storage, Lifecycle, and Environment Isolation

**Concepts demonstrated:** resource configuration, conditional expressions, `for_each`, lifecycle rules, tagging strategy.

### 3.1 S3 Module (`modules/s3/`)

Inputs: `bucket_name_prefix`, `environment`, `enable_versioning`, `lifecycle_enabled`
Outputs: `bucket_id`, `bucket_arn`, `bucket_domain_name`

### 3.2 Environment-Specific Buckets

Provision separate S3 buckets per environment using a naming convention:

```
{prefix}-{environment}-{aws_account_id}
```

- Enforce bucket name uniqueness with account ID interpolation
- Tag all resources with `Environment`, `ManagedBy = "terraform"`, `Project`

### 3.3 Versioning and Lifecycle Rules

- Enable versioning conditionally based on `var.enable_versioning`
- Configure lifecycle rule to transition objects to `STANDARD_IA` after 30 days and expire noncurrent versions after 90 days (dev) vs. 365 days (prod)

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "this" {
  count  = var.lifecycle_enabled ? 1 : 0
  bucket = aws_s3_bucket.this.id
  # ... rules
}
```

### 3.4 Public Access Block and Bucket Policy

- Block all public access on every bucket
- Attach a bucket policy enforcing HTTPS-only access (`aws:SecureTransport`)

### 3.5 Access Logging

Route S3 access logs from application buckets to a dedicated logging bucket — demonstrates defense-in-depth and audit trail thinking.

**SRE relevance:** Mirrors artifact/log storage patterns used in environment lifecycle management, including backup and retention policies.

---

## Stage 4 — DynamoDB: Application Data and State Store

**Concepts demonstrated:** NoSQL provisioning, capacity modes, TTL, stream configuration, tagging.

### 4.1 DynamoDB Module (`modules/dynamodb/`)

Inputs: `table_name`, `environment`, `billing_mode`, `enable_ttl`, `enable_streams`
Outputs: `table_arn`, `table_name`, `stream_arn`

### 4.2 Core Table Configuration

- Configure hash key and optional range key via variables
- Support both `PAY_PER_REQUEST` (dev/staging) and `PROVISIONED` (prod) billing modes using a conditional
- Enable point-in-time recovery (PITR) in prod

```hcl
resource "aws_dynamodb_table" "this" {
  name         = "${var.table_name}-${var.environment}"
  billing_mode = var.billing_mode
  hash_key     = var.hash_key

  point_in_time_recovery {
    enabled = var.environment == "prod" ? true : false
  }
}
```

### 4.3 TTL Configuration

Enable TTL on a configurable attribute for session or ephemeral data — demonstrate operational understanding of data expiration.

### 4.4 DynamoDB Streams (Stretch)

Enable DynamoDB Streams and output the stream ARN for downstream consumption (e.g., Lambda trigger) — demonstrates design awareness for event-driven patterns.

### 4.5 Environment-Differentiated Configuration

Show `terraform.tfvars` differences across environments:

| Setting | dev | staging | prod |
|---|---|---|---|
| `billing_mode` | PAY_PER_REQUEST | PAY_PER_REQUEST | PROVISIONED |
| `enable_pitr` | false | false | true |
| `enable_streams` | false | true | true |

**SRE relevance:** Demonstrates ability to differentiate infrastructure configuration per environment — a core requirement when operating many tenant environments.

---

## Stage 5 — Networking: VPC and Security Groups





---

## Stage 6 — Multi-Environment Orchestration



---

## Stage 7 — Observability and Monitoring


---

## Stage 8 — CI/CD Pipeline (GitHub Actions)


---

## Stage 9 — Terraform Operations and State Management

---

## Architecture Diagram

>
---

## How This Maps to the GitLab SRE JD

| JD Requirement | Demonstrated Here |
|---|---|
| Terraform modules, variables, state management for multiple environments | All phases |
| Infrastructure lifecycle: provisioning, upgrades, configuration changes | Phases 1–6, 8–9 |
| Reducing manual toil through automation | Phase 8 (CI/CD), Phase 9.2 (drift detection) |
| Observability stack | Phase 7 |
| Runbooks and repeatable operational processes | Phase 9, `docs/runbook.md` |
| Git-based IaC workflows | Phase 8, PR-driven plan/apply |
| IAM least-privilege and security | Phase 2 |
| Environment isolation | Phase 6, VPC module |

---

## Getting Started

### Prerequisites

- Terraform >= 1.6
- AWS CLI configured with appropriate credentials
- GitHub repository with Actions enabled
- (Optional) AWS account with sufficient IAM permissions to create all resources above

### Bootstrap (One-time)

```bash
cd bootstrap/
terraform init
terraform apply
```

### Provision an Environment

```bash
cd environments/dev/
terraform init
terraform plan
terraform apply
```

### Tear Down

```bash
terraform destroy
```

---

## License

MIT
