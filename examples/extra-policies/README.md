# Extra Policies Example

Creates an instance profile with an embedded permissions policy plus an existing
AWS managed policy (`CloudWatchAgentServerPolicy`) attached via `extra_policies`.

## Usage

```bash
terraform init
terraform apply -var environment=development -var region=us-west-2
```

## Cleanup

```bash
terraform destroy -var environment=development -var region=us-west-2
```
