# Examples

Common use cases for the module. Runnable versions of these examples live in the
[examples/](https://github.com/infrahouse/terraform-aws-instance-profile/tree/main/examples)
directory of the repository.

## Basic Profile

An instance profile with an embedded permissions policy:

```hcl
data "aws_iam_policy_document" "permissions" {
  statement {
    actions   = ["ec2:Describe*"]
    resources = ["*"]
  }
}

module "instance_profile" {
  source  = "registry.infrahouse.com/infrahouse/instance-profile/aws"
  version = "2.0.0"

  profile_name = "web-server"
  permissions  = data.aws_iam_policy_document.permissions.json
}
```

## Attach Existing Managed Policies

Attach AWS managed or customer managed policies in addition to the embedded one:

```hcl
module "instance_profile" {
  source  = "registry.infrahouse.com/infrahouse/instance-profile/aws"
  version = "2.0.0"

  profile_name = "monitoring-agent"
  permissions  = data.aws_iam_policy_document.permissions.json

  extra_policies = {
    cloudwatch = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
  }
}
```

## Disable SSM Access

By default the module attaches `AmazonSSMManagedInstanceCore`. Opt out:

```hcl
module "instance_profile" {
  source  = "registry.infrahouse.com/infrahouse/instance-profile/aws"
  version = "2.0.0"

  profile_name = "isolated-worker"
  permissions  = data.aws_iam_policy_document.permissions.json
  enable_ssm   = false
}
```

## Custom Role Name

Use an explicit role name instead of one generated from the profile name:

```hcl
module "instance_profile" {
  source  = "registry.infrahouse.com/infrahouse/instance-profile/aws"
  version = "2.0.0"

  profile_name = "my-instance-profile"
  permissions  = data.aws_iam_policy_document.permissions.json
  role_name    = "custom-ec2-role"
}
```

## With an Auto Scaling Group

Use the profile in a launch template for an Auto Scaling Group:

```hcl
module "instance_profile" {
  source  = "registry.infrahouse.com/infrahouse/instance-profile/aws"
  version = "2.0.0"

  profile_name = "asg-worker"
  permissions  = data.aws_iam_policy_document.permissions.json

  tags = {
    environment = var.environment
    service     = "worker"
  }
}

resource "aws_launch_template" "worker" {
  name_prefix   = "worker-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  iam_instance_profile {
    arn = module.instance_profile.instance_profile_arn
  }
}
```

## Granting Access To The Role From Other Resources

The role ARN output is useful in resource policies, e.g. allowing instances to read a
secret:

```hcl
module "instance_profile" {
  source  = "registry.infrahouse.com/infrahouse/instance-profile/aws"
  version = "2.0.0"

  profile_name = "app-server"
  permissions  = data.aws_iam_policy_document.permissions.json
}

module "app_secret" {
  source  = "registry.infrahouse.com/infrahouse/secret/aws"
  version = "1.1.1"

  secret_name = "app-config"
  readers = [
    module.instance_profile.instance_role_arn
  ]
}
```
