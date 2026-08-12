# Configuration

All input variables the module accepts, with examples.

## Required Inputs

### `profile_name`

Name of the instance profile. Also used to derive the role name (unless `role_name` is
set) and the policy name.

```hcl
profile_name = "web-server"
```

Names longer than AWS limits are truncated automatically — see
[Architecture → Naming](architecture.md#naming).

### `permissions`

A JSON permissions policy. The module creates a new IAM policy with this document and
attaches it to the instance role. Build it with an `aws_iam_policy_document` data source
rather than hand-written JSON:

```hcl
data "aws_iam_policy_document" "permissions" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::my-bucket/*"]
  }
}

module "profile" {
  # ...
  permissions = data.aws_iam_policy_document.permissions.json
}
```

## Optional Inputs

### `enable_ssm`

Default: `true`

Attaches the AWS-managed `AmazonSSMManagedInstanceCore` policy so the instance can be
managed through AWS Systems Manager (Session Manager shell access, patching, inventory).
Set to `false` if you don't want instances reachable via SSM:

```hcl
enable_ssm = false
```

### `extra_policies`

Default: `{}`

A map of additional policy ARNs to attach to the instance role. The key is a free-form
identifier (used as the attachment key), the value is the policy ARN:

```hcl
extra_policies = {
  cloudwatch = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
  backups    = aws_iam_policy.backups.arn
}
```

### `role_name`

Default: `null`

Explicit name for the instance role. When omitted, the role name is generated from
`profile_name` used as a prefix:

```hcl
role_name = "web-server-role"
```

!!! warning
    Unlike the generated prefix-based name, an explicit `role_name` must be unique in
    the AWS account. Two profiles with the same `role_name` will conflict.

### `tags`

Default: `{}`

A map of tags added to every resource the module creates:

```hcl
tags = {
  environment = "production"
  service     = "web"
}
```

### `upstream_module`

Default: `null`

If this module is called from another module, pass the caller's name here. It's recorded
in the `upstream_module` tag on created resources for provenance:

```hcl
upstream_module = "infrahouse/jumphost/aws"
```

## Outputs

| Output | Description |
|--------|-------------|
| `instance_profile_name` | Instance profile name — use in `aws_instance.iam_instance_profile`. |
| `instance_profile_arn` | Instance profile ARN — use in launch template `iam_instance_profile` blocks. |
| `instance_role_name` | Name of the created role — handy for attaching more policies later. |
| `instance_role_arn` | ARN of the created role — useful for resource policies (S3 buckets, secrets). |
| `instance_role_policy_name` | Name of the created permissions policy. |
| `instance_role_policy_arn` | ARN of the created permissions policy. |
| `instance_role_policy_attachment` | ID of the main policy attachment. |
