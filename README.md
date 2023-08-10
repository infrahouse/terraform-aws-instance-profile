# terraform-aws-instance-profile

The module conveniently bundles AWS resources to create an EC2 instance profile.

A user is asked to provide the instance profile name and permissions.

## Usage example

### Profile with embedded policy
First, let's prepare permissions the profile will have.
```hcl
data "aws_iam_policy_document" "jumphost_permissions" {
  statement {
    actions   = ["ec2:Describe*"]
    resources = ["*"]
  }
}
```
Now we're ready to create the instance profile.
```hcl
module "jumphost_profile" {
  source         = "infrahouse/instance-profile/aws"
  version        = "~> 1.0"
  permissions    = data.aws_iam_policy_document.jumphost_permissions.json
  profile_name   = "jumphost"
}
```
### Profile with extra policy

Let's say we want to create the instance profile and attach an existing policy to it.
This is the existing policy.
```hcl
data "aws_iam_policy_document" "package-publisher" {
  actions = [
    "s3:ListBucket",
    "s3:GetObject",
    "s3:PutObject",
    "s3:DeleteObject",
  ]
  resources = [
    "arn:aws:s3:::infrahouse-release-focal/*",
    "arn:aws:s3:::infrahouse-release-jammy/*"
  ]
}

resource "aws_iam_policy" "package-publisher" {
  name        = "package-publisher"
  description = "Policy that allows to publish packages"
  policy      = data.aws_iam_policy_document.package-publisher.json
}
```
And now we want to create the profile with the `package-publisher` policy attached to it.
```hcl
module "jumphost_profile" {
  source         = "infrahouse/instance-profile/aws"
  version        = "~> 1.0"
  permissions    = data.aws_iam_policy_document.jumphost_permissions.json
  profile_name   = "jumphost"
  extra_policies = {
    (aws_iam_policy.package-publisher.name) : aws_iam_policy.package-publisher.arn
  }
}
```
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.11 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | ~> 5.11 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_iam_instance_profile.profile](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_instance_profile) | resource |
| [aws_iam_policy.profile](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.profile](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.extra](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.profile](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_policy_document.assume](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_extra_policies"></a> [extra\_policies](#input\_extra\_policies) | A map of additional policy ARNs to attach to the instance role | `map(string)` | `{}` | no |
| <a name="input_permissions"></a> [permissions](#input\_permissions) | A JSON with a permissions policy. Note, a new policy will be created with these permissions. | `any` | n/a | yes |
| <a name="input_profile_name"></a> [profile\_name](#input\_profile\_name) | Instance profile name. | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_instance_profile_arn"></a> [instance\_profile\_arn](#output\_instance\_profile\_arn) | Instance profile ARN. |
| <a name="output_instance_profile_name"></a> [instance\_profile\_name](#output\_instance\_profile\_name) | Instance profile name. It's the same as the passed variable. |
