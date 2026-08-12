# terraform-aws-instance-profile

Terraform module that creates an AWS IAM instance profile together with its IAM role and
permissions policy, so an EC2 instance gets exactly the permissions it needs — in one module
call.

Published on the Terraform Registry as
[infrahouse/instance-profile/aws](https://registry.terraform.io/modules/infrahouse/instance-profile/aws/latest).

## What It Does

Attaching an IAM role to an EC2 instance requires several resources wired together: an IAM
role with an EC2 trust policy, a permissions policy, one or more policy attachments, and the
instance profile itself. This module bundles all of them:

- An **IAM role** assumable by `ec2.amazonaws.com`.
- An **IAM policy** created from the permissions JSON you pass in.
- An **instance profile** that carries the role.
- Policy **attachments** for the main policy, any extra policies, and (optionally) the
  AWS-managed `AmazonSSMManagedInstanceCore` policy.

## Features

- **Automatic SSM Integration**: Enables AWS Systems Manager access by default with the
  `AmazonSSMManagedInstanceCore` policy.
- **Custom Policy Support**: Attach your own IAM policies via JSON policy documents.
- **Additional Policies**: Attach existing AWS managed or customer managed policies.
- **Flexible Role Naming**: Use custom role names or auto-generated names based on the
  profile name.
- **Resource Tagging**: Apply consistent tags across all created IAM resources.
- **Safe Naming**: Role, policy, and profile names are truncated to respect AWS length
  limits.

## Quick Start

```hcl
data "aws_iam_policy_document" "permissions" {
  statement {
    actions   = ["ec2:Describe*"]
    resources = ["*"]
  }
}

module "instance_profile" {
  source  = "infrahouse/instance-profile/aws"
  version = "1.9.0"

  profile_name = "web-server"
  permissions  = data.aws_iam_policy_document.permissions.json
}

resource "aws_instance" "web" {
  # ...
  iam_instance_profile = module.instance_profile.instance_profile_name
}
```

## Where To Go Next

- [Getting Started](getting-started.md) — prerequisites and your first deployment.
- [Architecture](architecture.md) — what the module creates and how it fits together.
- [Configuration](configuration.md) — every input variable explained.
- [Examples](examples.md) — common use cases.
- [Troubleshooting](troubleshooting.md) — common issues and how to fix them.
