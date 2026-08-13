# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This repository is `terraform-aws-instance-profile`, an InfraHouse Terraform module (published to the Terraform
Registry as `infrahouse/instance-profile/aws`) that creates an IAM instance profile plus its role and policies
for EC2 instances.

## First Steps

**Your first tool call in this repository MUST be reading .claude/CODING_STANDARD.md.
Do not read any other files, search, or take any actions until you have read it.**
This contains InfraHouse's comprehensive coding standards for Terraform, Python, and general formatting rules.

## Commands

```bash
make bootstrap    # Install Python dev dependencies (pytest-infrahouse, infrahouse-core)
make lint         # terraform fmt --check -recursive
make format       # terraform fmt -recursive && black tests
make test-clean   # Run tests, destroy AWS resources after (run before submitting a PR)
make test-keep    # Run tests, keep AWS resources for debugging
make clean        # Remove terraform state/lock artifacts from test_data and pytest cache
```

Tests create **real AWS infrastructure**. `make test-keep`/`test-clean` run in `us-west-2` assuming the
`instance-profile-tester` IAM role (both defined at the top of the Makefile), so working AWS credentials are
required. To run a single parametrized case:

```bash
pytest -xvvs --aws-region=us-west-2 \
  --test-role-arn=arn:aws:iam::303467602807:role/instance-profile-tester \
  tests/test_module.py -k "aws_provider_version0 and foo"
```

## Architecture

The module itself is a flat set of root-level `.tf` files: an `aws_iam_role` assumable by `ec2.amazonaws.com`
(`data_sources.tf`), an `aws_iam_policy` built from the caller-supplied `permissions` JSON, the
`aws_iam_instance_profile`, and three policy attachments — the main policy, a `for_each` over `extra_policies`
ARNs, and an optional `AmazonSSMManagedInstanceCore` attachment gated by `enable_ssm` (all in `main.tf`).

### Versioning

The module version lives in three synchronized places: `.bumpversion.cfg`, `locals.tf`
(`local.module_version`, stamped into role tags), and the `version = "..."` strings in README.md examples.
`bumpversion` updates all three, commits, and tags — never edit version strings by hand. The changelog is
generated with git-cliff (`cliff.toml`) from conventional commits.

### How tests work

`tests/test_module.py` uses the `terraform_apply` fixture from pytest-infrahouse to apply the root config in
`test_data/instance-profile/`, which calls the module via `source = "../../"`. The test **overwrites**
`test_data/instance-profile/terraform.tf` and `terraform.tfvars` at runtime (it's parametrized over the AWS
provider version `~> 6.0` and over short/128-char-truncated profile names), so don't treat the
committed contents of those files as authoritative.

### Git hooks and generated files

`make install-hooks` (also triggered by bare `make`) symlinks `hooks/` into `.git/hooks`:

- `pre-commit` — enforces `terraform fmt`, regenerates the README section between `<!-- BEGIN_TF_DOCS -->` and
  `<!-- END_TF_DOCS -->` via terraform-docs, and requires trailing newlines on all files. To change the
  Requirements/Inputs/Outputs tables in README.md, edit the descriptions in the `.tf` files, not the README.
- `commit-msg` — rejects commit messages that don't follow Conventional Commits
  (`feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert|security`, optional scope, `!` for breaking).

`.claude/CODING_STANDARD.md`, `hooks/*`, and `.terraform-docs.yml` are managed centrally by the
[github-control](https://github.com/infrahouse/github-control) repository — do not edit them here; changes get
overwritten.
