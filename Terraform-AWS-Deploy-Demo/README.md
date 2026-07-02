# Terraform AWS Infrastructure Automation — SRE Portfolio Project

> **Purpose:** Demonstrates Infrastructure-as-Code proficiency using Terraform on AWS, covering beginner-to-intermediate concepts aligned with SRE environment automation roles. This project provisions multi-environment AWS infrastructure with a focus on modularity, state management, security, and operational best practices.

---

## Project Overview

This project provisions a realistic, multi-environment AWS infrastructure (e.g. dev / staging / prod) using Terraform. It demonstrates core SRE competencies including IaC lifecycle management, remote state, modular design, IAM least-privilege, and observability — mapped directly to the skills expected in environment automation roles.

**Tech Stack: PHASE 1 ** Terraform · AWS (IAM, S3, DynamoDB)**

**Tech Stack: PHASE 2 ** Terraform · AWS (EC2, VPC, CloudWatch) · GitHub Actions CI/CD**

---

## Repository Structure

```
Terraform-AWS-Deploy-Demo/
├── README.md
├── bootstrap-backend/              # Use this directory for the remote state storage infrastructure.
│   │   ├── main.tf
│   │   ├── provider.tf
│   │   ├── terraform.tfstate
│   │   ├── variables.tf
│   │   └── .terraform/
├── modules/
│   ├── ## Phase 1 ##               # Phase 1: Infrastructure Provisioning
│   ├── iam/
│   │   ├── main.tf
│   │   ├── policies.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── s3/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── dynamodb/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ## Phase 2 ##               # Phase 2: Infrastructure Provisioning
│   ├── ec2/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── monitoring/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/              
│   ├── dev/                                
│   │   ├── providers.tf
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   ├── terraform.tfstate       # Will be deleted after backend configuration is complete.
│   │   └── backend.tf
│   ├── staging/                    # (Not used in this demo.)
│   │   ├── providers.tf
│   │   ├── main.tf
│   │   ├── ...                    
│   └── prod/                   
│       ├── providers.tf
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       ├── terraform.tfstate       # Will be deleted after backend configuration is complete.
│       └── backend.tf
└── .gitignore
```

---

## Stage 1 — Terraform Foundations & AWS Remote State Bootstrap

**Concepts demonstrated:** Credential setup and storage, provider configuration, backend setup for S3 state storage, state locking and S3 versioning enabled.


### 1.1 AWS Access Credentials

Access to AWS resources from any location requires credentials stored in environment variables or in a shared credentials file. 

- Download the AWS CLI for platform-specific usage: [AWS Getting Started](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
- Confirm succuessful installation by running `aws --version`
  - For this demo, we'll use the AWS CLI v2. 
    - > aws-cli/2.35.11 Python/3.14.5 Darwin/25.5.0 exe/arm64
- Generate an access key pair and configure the AWS CLI with the credentials
  - From IAM Service -> IAM Users, click on your user name, navigate to the Security Credentials tab, and click Create Access Key.
  - Select your use case and select confirmation. For this demo, the use case is "Command Line Interface". 
  - Provide a Description tav value: "aws-access-from-local-terminal", the select "Create access key".
  - Copy the Access Key ID and Secret Access Key values.
  - Run `aws configure` and paste the Access Key ID and Secret Access Key values.
    - Set your default region
    - Set the output format. For this demo, the default will be kept as "json".
  - Login into AWS using the configured credentials.
  - Run `aws login`. Follow the prompts to authenticate.
  - Confirm the configuration by running `aws sts get-caller-identity`.
    - You should see the following output:
  ```json
  {
    "UserId": "<access-key-id>",
    "Account": "<6-digit-account-id>",
    "Arn": "arn:aws:sts::..."
  } 
  ```

### 1.2 Provider Configuration

Setting up the provider configuration will enable you to:
- Source and version providers from the Terraform registry.
- Configure and authenticate providers.
- Upgrade provider versions safely. 
- Configure multiple instances of the same provider using aliases and control which providers your Terraform modules use to provision infrastructure.

The following block configures:
- AWS as the provider, `source` of the provider pluggins as `[hostname]/namespace/type`,  and any `version` above 6.50.0. Any changes or new constraints on the provider version are made here.
  - `source` is the address of the provider on the Terraform registry.
  - `version` is the version constraint for the provider.
  - `required_version` is the minimum required version of Terraform or anything greater than or equal to 1.2 ("Major: 1, Minor: 2"). For this demo we will be using Terraform Community Edition 1.15.7. 
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.50.0"
    }
  }
  required_version = ">= 1.2"
}
```
The next block configures:
- A `region` for AWS resources. In the block below, region will be sourced from the `aws_region` in `variable.tf`.  It will be a function of the namespace being created, which will have a specific region assigned
```hcl
provider "aws" {
  region = var.aws_region
}
```
The completed provider.tf file should look like this:
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.50.0"
    }
  }
  required_version = ">= 1.2"
}

provider "aws" {
  region = var.aws_region
}
```
The final configuration above will be placed in the `providers.tf` file in each environment directory below:
- `bootstrap-backend/provider.tf`
- `environments/dev/provider.tf`
- `environments/staging/provider.tf`   (Not used in this demo)
- `environments/prod/provider.tf`

Select the `environments/dev/` directory and run `terraform init` to initialize the provider configuration.  This will download the provider plugins and store them in the `.terraform/providers/...` directory.

```
... % tf init
Initializing provider plugins found in the configuration...
- Finding hashicorp/aws versions matching "~> 6.50.0"...
- Installing hashicorp/aws v6.50.0...
- Installed hashicorp/aws v6.50.0 (signed by HashiCorp)

Initializing the backend...


Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

```
```
├── environments/              
│   ├── dev/                                
│   │   ├── providers.tf
│   │   ├── .terraform
│   │   .     └── providers
│   │   .     .    └── <hostname=registry.terraform.io>
│   │   .     .    .     └── <namespace=hashicorp>
│   │   .     .    .     .      └── <type=aws>

```

### 1.3 S3 Backend for Remote State

Provision an S3 bucket to store Terraform state files remotely:

- Enable versioning on the state bucket (supports state rollback)
- Enable server-side encryption (SSE-S3 or SSE-KMS)
- Block all public access

<br>

#### S3 Bucket Creation

Documents used to create the S3 bucket, enable versioning, enable encryption, and block public access:
- [S3 Bucket Creation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket)
- [S3 Bucket Encryption](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration#sse_algorithm-2
)
- [S3 Bucket Public Access Block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_public_access_block)
- [S3 Bucket Versioning](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_versioning)

1. Create a `main.tf` file in the `bootstrap-backend/` directory with the following content:
```hcl
# bootstrap-backend/main.tf
**== main.tf ==**
```hcl
# The Single S3 Bucket for both State Storage AND Native Locking
resource "aws_s3_bucket" "terraform_state" {
  bucket_prefix = "terraform-aws-remote-tfstate-bucket"
  force_destroy = false
}

# DevSecOps Best Practice: Ensure the state bucket is fully encrypted
resource "aws_s3_bucket_server_side_encryption_configuration" "tfstate_crypto" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# DevSecOps Best Practice: Block all public access to your state file
resource "aws_s3_bucket_public_access_block" "tfstate_privacy" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable versioning
resource "aws_s3_bucket_versioning" "state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}
        

```

2. Perform Terraform workflow commands:
  - `tf init` to initialize the provider plugins and download the state bucket.
  - `tf plan` to preview the changes that will be made to the state bucket.
  - `tf apply` to create the state bucket and configure its settings.

3. To see the bucket that was just created:
```bash
..% aws s3 ls

NOTE: The output will be suppled to "bucket" in the backend.tf file.
```
...as viewed from the UI-Console:

[paste-s3-bucket-image-here]

<br>



### 1.4 Backend Configuration Per Environment

Configure the `dev` and `prod` environments to use the shared S3 backend with a unique state key:
Note the 

* **/evnironments/dev/backend.tf**
```hcl
# environments/dev/backend.tf
terraform {
  backend "s3" {
    bucket         = "terraform-aws-remote-tfstate-bucket20260702004645306300000001"
    key            = "environments/dev/terraform.tfstate"
    region         = "us-east-1"
    use_lockfile   = true
  }
}
```
* **/evnironments/prod/backend.tf**
```hcl
# environments/dev/backend.tf
terraform {
  backend "s3" {
    bucket         = "terraform-aws-remote-tfstate-bucket20260702004645306300000001"
    key            = "environments/prod/terraform.tfstate"
    region         = "us-east-1"
    use_lockfile   = true
  }
}
```

2. Perform Terraform `init` in both environments:
- `tf init` to configure the s3 backend.
```
... % tf init

You should see the following output:

Initializing provider plugins found in the configuration...
- Reusing previous version of hashicorp/aws from the dependency lock file
- Using previously-installed hashicorp/aws v6.50.0

Initializing the backend...

Successfully configured the backend "s3"! Terraform will automatically
use this backend unless the backend configuration changes.



Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

```
3. At this point you will see the successful creation of the S3 backend, however no state has been created. We can create a local file in the directories to force a state file to be created.

* **/evnironments/dev/main.tf**
```hcl
# environments/dev/backend.tf
resource "local_file" "change_state" {
  filename = "demofile.txt"
  content  = "Demo file to force a state file to be generated."
}
```
* **/evnironments/prod/main.tf**
```hcl
# environments/dev/backend.tf
resource "local_file" "change_state" {
  filename = "demofile.txt"
  content  = "Demo file to force a state file to be generated."
}
```

4. Perform Terraform workflow commands in both the `dev` and `prod` environments:
  - `tf init` to initialize the provider plugins and download the state bucket.
  - `tf plan` to preview the changes that will be made to the state bucket.
  - `tf apply` to create the state bucket and configure its settings.

5. Now you can see the state files in the S3 bucket:
```bash

...% aws s3 ls s3://terraform-aws-remote-tfstate-bucket20260702004645306300000001 --recursive

2026-07-01 22:10:42       1686 environments/dev/terraform.tfstate
2026-07-01 22:15:29        181 environments/prod/terraform.tfstate
```

<br>


---

## Stage 2 — IAM: Identity and Least-Privilege Access

**Concepts demonstrated:** IAM roles, policies, instance profiles, policy attachment, data sources, least-privilege design.

Documents used to create the IAM: role, policies, policy document, and policy attachment:

- [IAM Role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role)
- [IAM Policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy)
- [IAM Policy Document](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document)
- [IAM Policy Attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy_attachment)

### 2.1 IAM Module Structure (`modules/iam/`)

- Accept `environment` and `app_name` as input variables
- Output role ARN and instance profile name for consumption by other modules

In this section we are going to look at the structure of what makes a module.  A module is a collection of resources that can be used in 

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


**SRE relevance:** Demonstrates understanding of isolation and least-privilege — critical when managing many tenant environments where blast radius must be minimized.

---

## Stage 3 — S3: Storage, Lifecycle, and Environment Isolation

- [S3 Bucket Creation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket)


---

## Stage 4 — DynamoDB: Application Data and State Store

- [DynamoDB Table Creation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table)
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


## How This Maps to the GitLab SRE JD


---

## Getting Started

### Prerequisites

- Terraform >= 1.6 (Community Edition Latest = 1.15.7)
- Terraform Cloud ( Optional
- AWS CLI configured with appropriate credentials
- GitHub repository with Actions enabled
- AWS account with sufficient IAM permissions to create all resources above

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
