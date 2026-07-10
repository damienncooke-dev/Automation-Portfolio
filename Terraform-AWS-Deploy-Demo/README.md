# Terraform AWS Infrastructure Automation — SRE Portfolio Project

> **Purpose:** Demonstrates Infrastructure-as-Code proficiency using Terraform on AWS, covering beginner-to-intermediate concepts aligned with SRE environment automation roles. This project provisions multi-environment AWS infrastructure with a focus on modularity, state management, security, and operational best practices.

---

## Project Overview

This project provisions a realistic, multi-environment AWS infrastructure (e.g. dev / prod) using Terraform. It demonstrates core SRE competencies including IaC lifecycle management, remote state, modular design, IAM least-privilege, and observability — mapped directly to the skills expected in environment automation roles.

[Project PHASE 1 - Create a remote state backend (RSB) for storing Terraform state files in S3.](#phase-1--terraform-foundations--aws-remote-state-bootstrap)

[Project PHASE 2 - Create IAM role and policies to manage multi-market ec2 access to AWS resources.](#phase-2--role-identity-policies-least-privilege-access-and-multi-tenancy-deployment)


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
│   ├── ec2/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── market/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
├── environments/              
│   ├── dev/                                
│   │   ├── providers.tf
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfstate       # Will be copied to remote state backup after backend configuration is complete, and deleted from local
│   │   └── backend.tf                 
│   └── prod/                   
│       ├── providers.tf
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfstate       # Will be copied to remote state backup after backend configuration is complete, and deleted from local
│       └── backend.tf
├── sampple-data/              
│   ├── sample-app.log  
│   └── sample-dynamodb-item.json  
└── .gitignore
```

---

## Phase 1 — Terraform Foundations & AWS Remote State Bootstrap

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
<br>

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
<br>

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

1. Configure the `dev` and `prod` environments to use the shared S3 backend with a unique state key:
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

## Phase 2 —  Role Identity, Policies, Least-Privilege Access, and Multi-Tenancy Deployment

The following sections will walk through the creation of a "market_stack" that groups together the resources needed to create the deployment of a storage and indexing solution for EC2 instances in `Prod` and `Dev` environments.  The prod and dev environments are separated by region, (us-east-1-Dev and us-west-1-Prod), and within those environments you also have multi-tenant, specific market regions, that align development and production artifacts to the market in which they belong.

The market_stack will consist of the following resources:
- An S3 bucket for log storage in each region-specific market; (market-a, market-b, and market-c). The markets will exist for both dev and prod environments.  
- DynamoDB table for log file indexing / metadata tracking, also market-specific and environment-specific. 
- One EC2 instance per region-specific (market-a,  market-b, and market-c) with access to specific S3 and DynamoDB resources in both Dev and Prod environments.
- An IAM role called 'market_role' to allow the EC2 instances access to their designated S3 bucket and DynamoDB table.
- IAM policy document and instance for: 
  - Allowing EC2 to assume 'market_role' (Trust Policy)
  - Giving permission to 'market_role' to perform actions on the S3 bucket and DynamoDB table.
  - Access to SSM session manager (SSM) for EC2 CLI access. 

**Concepts demonstrated:** IAM role, policies, instance profiles, multi-tenancy, and least-privilege design 

**Documents used to create the deployment resources:**

- [IAM Role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role)
- [IAM Policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy)
- [IAM Policy Document](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document)
- [IAM Policy Attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy_attachment)
- [S3 Bucket Creation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket)
- [DynamoDB Table Creation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table)
- [EC2 Instance Creation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance)

<br>

```
                                                    MARKET STACK ARCHITECTURE
                                       
 
                           Dev (us-east-1)                                           Prod (us-west-1)
                                  |                             |                            |
                                  |                             |                            |
               +------------------+------------------+          |         +------------------+------------------+
               |                  |                  |          |         |                  |                  |
            market-a           market-b           market-c      |      market-a           market-b           market-c
               |                  |                  |          |         |                  |                  |
              EC2                EC2                EC2         |        EC2                EC2                EC2     
               |                  |                  |          |         |                  |                  |             
        [market-a-role]    [market-b-role]    [market-c-role]   |  [market-a-role]    [market-b-role]    [market-c-role]
               +                  +                  +          |         +                  +                  +    
       [market-a-policy]  [market-b-policy]  [market-c-policy]  | [market-a-policy]  [market-b-policy]  [market-c-policy]              
               |                  |                  |          |         |                  |                  |       
           S3 bucket          S3 bucket          S3 bucket      |     S3 bucket          S3 bucket          S3 bucket
               &                  &                  &          |         &                  &                  &
           DynamoDB           DynamoDB           DynamoDB       |     DynamoDB           DynamoDB           DynamoDB
             table              table              table        |       table              table              table
                         
                         
```

 

### Development Environment Allowed Actions
| Dev-Role      | Dev: market-a <br/> Stack | Dev: market-b <br/> Stack  | Dev: market-c <br/> Stack  | Prod: market-a <br/> Stack  | Prod: market-b <br/> Stack  | Prod: market-c  <br/> Stack  |
|---------------|:-------------------------:|:--------------------------:|:--------------------------:|:---------------------------:|:---------------------------:|:----------------------------:|
| market-role-a |          *Allow*          |             No             |             No             |             No              |             No              |              No              |
| market-role-b |            No             |          *Allow*           |             No             |             No              |             No              |              No              |
| market-role-c |            No             |             No             |          *Allow*           |             No              |             No              |              No              |

### Production Environment Allowed Actions
| Prod-Role     |Dev: market-a <br/> Stack  | Dev: market-b <br/> Stack  | Dev: market-c <br/> Stack  | Prod: market-a <br/> Stack  |Prod: market-b  <br/> Stack  | Prod: market-c  <br/> Stack  |
|---------------|:-------------------------:|:--------------------------:|:--------------------------:|:---------------------------:|:---------------------------:|:----------------------------:|
| market-role-a |            No             |             No             |             No             |           *Allow*           |             No              |              No              |
| market-role-b |            No             |             No             |             No             |             No              |           *Allow*           |              No              |
| market-role-c |            No             |             No             |             No             |             No              |             No              |           *Allow*            |


<br>



### 2.1  Module Structure 

Modules are a Terraform feature that allows you to break down complex infrastructure into reusable, modular pieces.  The main benefits of using modules here are that you are able to break large configurations into logical units that can reused over and over again, and you can isolate the reusable infrastructure logic from the environment-specific deployment configuration.  This means that you can create as many environments as needed without touching the infrastructure part and you can modify and test the infrastructure part without impacting the environment configuration. 

The module structure in this demo is as follows:
- Environment Specific Modules
  - One root module that passes in environment-specific variables to a composition layer module before calling the individual module resources.
- Infrastructure Logic
  - The composition layer module is responsible for creating the resources as a "stack" of modules.  It also orchestrates the passing of input and output variables to the individual module resources.
  - The individual module resources are responsible for creating the resources needed for the environment.

<br>
  
**Actual module structure implementation:**
```hcl

# main root module that passes in environment-specific variables to a composition layer module.
-> `environments/[dev|prod]/main.tf`  
        
module "market_stack" {
  source           = "../../modules/market"
  for_each         = toset(var.market_region) # for_each only accepts map and set types, raw list types generate an error.
  market_region    = each.value   # Values are {market-a, market-b, market-c}
  environment      = var.environment  # self = prod
  trusted_role_arn = var.trusted_role_arn   # Allows any IAM principle that has Assume Role enabled on their account to assume any of the market roles. 'trusted_role_arn' is picked up from ENV setting: 'TF_VAR_trusted_role_arn'
  billing_mode     = var.billing_mode   # Set to PAY-PER-USE
  ami_id           = var.ami_id   # Configured OS used to apply to EC2 instance.  Specific to aws_region
  force_destroy    = var.force_destroy  # Prevents accidental deletion of data when 'false', allows complete resource removal including data when 'true'
}
```

```hcl
# composition layer module that stacks the required modules and orchestrates the passing of input and output variables to the individual module resources.
-> `modules/market/main.tf`

module "s3" {
  source           = "../s3"
  environment      = var.environment
  market_region    = var.market_region
  force_destroy    = var.force_destroy
}

module "dynamodb" {
  source           = "../dynamodb"
  environment      = var.environment
  market_region    = var.market_region
  billing_mode     = var.billing_mode
}

module "ec2" {
  source           = "../ec2"
  environment      = var.environment
  market_region    = var.market_region
  ami_id           = var.ami_id   # Passed through from calling 'root' module. Specifies OS to be used in EC2
  iam_instance_profile   = module.iam.instance_profile_name   # Gets value from the 'output' of the iam module
}

module "iam" {
  source           = "../iam"
  environment      = var.environment
  market_region    = var.market_region
  bucket_arn       = module.s3.bucket_arn      # Gets value from the 'output' of the S3 module
  table_arn        = module.dynamodb.table_arn # Gets value from the 'output' of the dynamodb module
  trusted_role_arn = var.trusted_role_arn      # Passed through from calling 'root' module
}


```

```
# individual module resources that create the resources needed for the environment.
- `modules/s3/`
- `modules/dynamodb/`
- `modules/ec2/`
- `modules/iam/`
```

<br>

### 2.2 IAM Role for s3 Bucket and DynamoDB Table access (Instance Profile)
 
The IAM role is needed to enable access to resources and what actions are permitted on them.  IAM roles have no meaning until policies are attached to them. 

- Create an IAM role with an EC2 trust policy.  The trust policy is required by AWS and must be attached to the role before it can be assumed.  


```hcl
# Main module that creates the IAM role and instance profiles. The policies.tf file contains the custom policy data used by main.tf.
-> `modules/iam/main.tf`

# The 'resource' below creates the role "demo-${var.environment}-${var.market_region}-role" and attaches the trust policy. 
resource "aws_iam_role" "market_role" {
  name               = "demo-${var.environment}-${var.market_region}-role"
  path               = "/market/"   # organize this role under "market"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role_policy.json
}
      ...
        
# The data block below is specifically for the trust policy required for the 'aws_iam_role' resource above.        
-> `modules/iam/policies.tf`
        
# Trust Policy
data "aws_iam_policy_document" "ec2_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]  # Required for all roles

    principals {
      type        = "Service"  # Trust AWS service listed as 'identifiers' to assume role
      identifiers = ["ec2.amazonaws.com"]
    }
    principals {
      type        = "AWS"     # Trust AWS entity provided in "identifiers" to assume role
      identifiers = [var.trusted_role_arn]  # This value is picked up by the calling root module and passed to iam. 
    }
  }
}
        ...
                
                



```
<br>

### 2.3 Use custom IAM Policies to define access and permissions (Least Privilege)

- Create a custom policy in a separate `policies.tf` file granting only the permissions needed (e.g., read from a specific S3 bucket, write to a specific DynamoDB table). 
- Create an instance profile to attach the role to policies defining resource permissions.
- Create an instance profile to associate the role with the EC2 instance.
- Attach an AWS managed policy (AmazonSSMManagedInstanceCore) to allow ssh into the EC2 instance.

```hcl
# The data block below is specifically for the trust policy required for the 'aws_iam_role' resource above.        
-> `modules/iam/policies.tf`
   
# Permission Policy
data "aws_iam_policy_document" "market_permissions" {
   # The 'statement' blocks below are the policy configurations for S3 and DynamoDB
   statement{
     sid = "S3ListBucket"
     actions = [
        "s3:ListBucket"
     ]
     resources = [
        var.bucket_arn    #  list only permitted and known bucket resources (e.g. arn:aws:s3:::demo-dev-market-a-logs)
     ]
   }

   statement{
     sid = "S3Access"
     actions = [
        "s3:GetObject",
        "s3:PutObject"
     ]
     resources = [
        "${var.bucket_arn}/*"   # actions allowed only on the objects in the bucket with arn (e.g. arn:aws:s3:::demo-dev-market-a-logs/*)
     ]
   }

   statement{
     sid = "DynamodDBAccess"
     actions = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:DescribeTable"
     ]
     resources = [
        var.table_arn   # actions allowed on tables with arn (e.g. arn:aws:dynamodb:us-east-1:...:table/demo-dev-market-a-log-index
     ]
   }
}


```
```hcl
# Main module that creates the IAM role and instance profiles. The policies.tf file contains the custom policy data used by main.tf.
-> `modules/iam/main.tf`

# The 'resource' below creates the role "demo-${var.environment}-${var.market_region}-role" and attaches the trust policy. 
resource "aws_iam_role" "market_role" {
         ...
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


```

<br>


### 2.4 Demonstrate Cross-Module Reference

A key feature of modules is the concept of cross-module references. In the example below, I will walk through how the IAM module consumes outputs from the S3 and DynamoDB modules to scope permissions to exact resource ARNs instead of using wildcards.

#### Step 1:
The workflow begins with either the dev or prod environments.  They both create the same resources and policies, just with differentiating names and environment-specific variables. Below the `environments/prod/main.tf` is shown with the values passed to the `module/market`

```hcl
# The main root module that calls the the market module.        
-> `environments/prod/main.tf`

module "market_stack" {
  source           = "../../modules/market"
  for_each         = toset({"market-a", "market-b", "market-c"}) # for_each only accepts map and set types, raw list types generate an error
  market_region    = "market-a" | "market-b" | "market-c"  # each of these values are passed to the module/market individually 
  environment      = "prod"
  trusted_role_arn = # provided by ENV variable TF_VAR_trusted_role_arn
  billing_mode     = "PAY_PER_REQUEST"
  ami_id           = "ami-07fdf51168766b58a"
  force_destroy    = false
}
```
<br>

#### Step 2:
The`module/market` will take the above values and use them to create the resources: (for the purposes of this demo, we will stick to module/iam)

```hcl
# The root module that calls the individual modules.        
-> `modules/market/main.tf`

  ...
        
module "iam" {
  source           = "../iam"
  environment      = "prod"
  market_region    = "market-a"  # We will use 'market-a' for the example
  bucket_arn       = module.s3.bucket_arn      # Gets value from the 'output' of the S3 module
  table_arn        = module.dynamodb.table_arn # Gets value from the 'output' of the dynamodb module
  trusted_role_arn = var.trusted_role_arn      # Passed through from calling 'root' module
}

  ...

```
<br>

#### Step 3:
The `bucket_arn` and `table_arn` values above are passed to the `iam` module, which are sourced from the `output.tf` file of the `s3` and `dynamodb` modules.

```hcl
# Values exported when creating the s3 bucket.        
-> `modules/s3/outputs.tf`
        
output "bucket_arn" {
  description = "ARN of bucket"
  value = aws_s3_bucket.app_logs.arn  # value is generated after the 'terraform apply' command is run
}

# This output value is picked up by the 'iam' module -> "bucket_arn = module.s3.bucket_arn = aws_s3_bucket.app_logs.arn"

```
```hcl
# Values exported when creating the dynamodb table.        
-> `modules/dynamodb/outputs.tf`
        
output "table_arn" {
  description = "ARN of table"
  value = aws_dynamodb_table.log_index.arn   # value is generated after the 'terraform apply' command is run
}

# This output value is picked up by the 'iam' module -> "table_arn = module.dynamodb.table_arn = aws_dynamodb_table.log_index.arn"

```
<br>

#### Step 4:
The `module/iam` uses the `bucket_arn` and `table_arn` values passed to it to assign the permission to the specific resource ARNs.  This is done in the `policies.tf` file.
```hcl
# The data block below is used to assign the permission policy to specific resource ARNs.        
-> `modules/iam/policies.tf`
  
data "aws_iam_policy_document" "market_permissions" {
   # The 'statement' blocks below are the policy configurations for S3 and DynamoDB
   statement{
     sid = "S3ListBucket"
     actions = [
        "s3:ListBucket"
     ]
     resources = [
        var.bucket_arn    # <--- Passed through from the calling root module module/market/main.tf 
     ]
   }

   statement{
     sid = "S3Access"
     actions = [
        "s3:GetObject",
        "s3:PutObject"
     ]
     resources = [
        "${var.bucket_arn}/*"   # <--- Passed through from the calling root module module/market/main.tf
     ]
   }

   statement{
     sid = "DynamodDBAccess"
     actions = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:DescribeTable"
     ]
     resources = [
        var.table_arn   # <--- Passed through from the calling root module module/market/main.tf
     ]
   }
}


```

#### Step 5:

We can quickly verify that the ARNs supplied by the S3 and DynamoDB were successfully assigned the permissions indicated above by looking at the AWS console `IAM -> Policies -> demo-prod-market-a-policy.` 

[paste dynamodb image here]


[paste s3 image here]


---
<br>

### 2.5 Demonstrate how the concept of multi-tenancy works in Terraform

In this final section, we will use the AWS UI Console to show how the concept of how multi-tenancy works by performing verifications of the following scenarios:

- Show how the IAM role is scoped to a specific region.



- Show how the EC2 instances are scoped to a specific region.



- Show the roles associated with the EC2 instances.



- Demonstrate how isolation of the environments prevents cross-tenant access.



---

## Getting Started

### Prerequisites

- Terraform >= 1.6 (Community Edition Latest = 1.15.7)
- AWS CLI configured with appropriate credentials
- GitHub repository 
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


BEST PRACTICES

🚨 Never share:

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_SESSION_TOKEN
* Private keys (.pem files)
* Terraform state files containing secrets
* Database passwords
* API keys/tokens
