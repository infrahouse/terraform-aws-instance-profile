---
name: Bug report
about: Report a problem with the module
title: ''
labels: bug
assignees: ''
---

## Describe the bug

A clear and concise description of what the bug is.

## To Reproduce

Module call that triggers the problem:

```hcl
module "instance_profile" {
  source  = "infrahouse/instance-profile/aws"
  version = "x.y.z"
  # ...
}
```

Steps:

1. `terraform apply`
2. See error

## Expected behavior

What you expected to happen.

## Actual behavior

What actually happened. Include the full error output:

```text

```

## Environment

- Module version:
- Terraform version (`terraform version`):
- AWS provider version:
