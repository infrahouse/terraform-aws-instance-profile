# Getting Started

This guide walks you through deploying your first instance profile with the module.

## Prerequisites

- **Terraform** with the AWS provider `>= 5.11, < 7.0`.
- **AWS credentials** with permissions to manage IAM resources:
  `iam:CreateRole`, `iam:CreatePolicy`, `iam:CreateInstanceProfile`,
  `iam:AttachRolePolicy`, `iam:AddRoleToInstanceProfile`, `iam:TagRole`,
  `iam:TagPolicy`, `iam:TagInstanceProfile`, and the corresponding read/delete
  actions for plan and destroy.
- An AWS account and a configured provider block:

```hcl
provider "aws" {
  region = "us-west-2"
}
```

!!! note
    IAM is a global service — the resources this module creates are not
    region-specific, but the provider still needs a region configured.

## First Deployment

### 1. Define the permissions

Describe what the EC2 instance is allowed to do with an
`aws_iam_policy_document` data source:

```hcl
data "aws_iam_policy_document" "permissions" {
  statement {
    actions   = ["ec2:Describe*"]
    resources = ["*"]
  }
}
```

### 2. Call the module

```hcl
module "instance_profile" {
  source  = "registry.infrahouse.com/infrahouse/instance-profile/aws"
  version = "1.9.0"

  profile_name = "my-first-profile"
  permissions  = data.aws_iam_policy_document.permissions.json
}
```

### 3. Apply

```bash
terraform init
terraform plan
terraform apply
```

Terraform creates the IAM role, the permissions policy, the instance profile, and the
policy attachments (including `AmazonSSMManagedInstanceCore`, since `enable_ssm`
defaults to `true`).

### 4. Verify

```bash
aws iam get-instance-profile --instance-profile-name my-first-profile
```

You should see the profile with one role attached.

### 5. Use the profile

Attach it to an EC2 instance, launch template, or Auto Scaling Group:

```hcl
resource "aws_instance" "web" {
  ami                  = data.aws_ami.ubuntu.id
  instance_type        = "t3.micro"
  iam_instance_profile = module.instance_profile.instance_profile_name
}
```

or

```hcl
resource "aws_launch_template" "web" {
  # ...
  iam_instance_profile {
    arn = module.instance_profile.instance_profile_arn
  }
}
```

## Next Steps

- Review all input variables in [Configuration](configuration.md).
- Browse common use cases in [Examples](examples.md).
- Learn what the module creates in [Architecture](architecture.md).
