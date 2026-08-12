# Basic Example

Creates an instance profile with an embedded permissions policy. SSM access is enabled
by default, so instances launched with this profile can be managed via AWS Systems
Manager Session Manager.

## Usage

```bash
terraform init
terraform apply -var environment=development -var region=us-west-2
```

## Cleanup

```bash
terraform destroy -var environment=development -var region=us-west-2
```
