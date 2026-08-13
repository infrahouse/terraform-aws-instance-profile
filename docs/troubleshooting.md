# Troubleshooting

Common issues when using the module and how to resolve them.

## `EntityAlreadyExists` when creating the role or profile

```text
Error: creating IAM Instance Profile (web-server): EntityAlreadyExists:
Instance Profile web-server already exists.
```

Instance profile names are unique per AWS account. Either pick a different
`profile_name`, or — if the leftover profile is from a destroyed stack that failed to
clean up — delete it manually:

```bash
aws iam delete-instance-profile --instance-profile-name web-server
```

The same applies to an explicit `role_name`: it must be unique in the account. When
`role_name` is omitted, the module uses a name *prefix* and Terraform appends a random
suffix, so generated names don't collide.

## Instance can't reach AWS APIs despite the profile being attached

The instance profile only provides credentials. Check that:

1. The instance can reach the AWS API endpoints (internet route, NAT gateway, or VPC
   endpoints).
2. The permissions JSON actually allows the actions your application performs. Inspect
   the policy:

   ```bash
   aws iam get-policy-version \
     --policy-arn <instance_role_policy_arn output> \
     --version-id v1
   ```

3. The application isn't using different credentials (environment variables and shared
   credentials files take precedence over IMDS).

## Instance doesn't appear in SSM / Session Manager

`enable_ssm = true` (the default) grants the IAM permissions, but SSM also requires:

- The SSM agent running on the instance (preinstalled on Amazon Linux and Ubuntu AMIs).
- Network access to the SSM endpoints (`ssm.*`, `ssmmessages.*`, `ec2messages.*`) via
  internet or VPC endpoints.

If the instance was already running when the profile was attached or changed, restart
the SSM agent — it caches credentials:

```bash
sudo systemctl restart amazon-ssm-agent # or snap.amazon-ssm-agent.amazon-ssm-agent
```

## `ec2tagger: Unable to describe ec2 tags` in the CloudWatch agent log

```text
ec2tagger: Unable to describe ec2 tags for initial retrieval
UnauthorizedOperation: You are not authorized to perform this operation.
```

The CloudWatch agent's ec2tagger needs `ec2:DescribeTags` to resolve the
`AutoScalingGroupName` metric dimension. The module grants this permission by default,
so if you see this error, the instance is running a profile created by an older module
version — upgrade the module and re-apply, or add the action to your `permissions`
document.

## `MalformedPolicyDocument` on apply

```text
Error: creating IAM Policy: MalformedPolicyDocument
```

The `permissions` input isn't a valid IAM policy JSON. Build it with the
`aws_iam_policy_document` data source instead of hand-written or `jsonencode()`-generated
JSON — the data source validates structure and produces correct formatting:

```hcl
data "aws_iam_policy_document" "permissions" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::my-bucket/*"]
  }
}
```

## New instance profile not usable immediately

IAM is eventually consistent. If an EC2 instance or Auto Scaling Group launch fails right
after the profile is created with an error like `Invalid IAM Instance Profile`, retry
after a few seconds. Within one Terraform configuration, reference module outputs
(`module.<name>.instance_profile_name`) rather than hard-coded names so Terraform orders
the operations correctly.

## `DeleteConflict` when destroying

```text
Error: deleting IAM Role: DeleteConflict: Cannot delete entity, must remove roles
from instance profile first.
```

Usually caused by resources outside Terraform still using the role or profile (e.g., an
instance launched manually). Detach or terminate those first, then re-run
`terraform destroy`.

## Getting Help

- [Open an issue](https://github.com/infrahouse/terraform-aws-instance-profile/issues)
- [Contact InfraHouse](https://infrahouse.com/contact)
