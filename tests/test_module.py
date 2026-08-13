import json
from os import path as osp, remove
from textwrap import dedent

import pytest
from pytest_infrahouse import terraform_apply

from tests.conftest import (
    LOG,
    TERRAFORM_ROOT_DIR,
)


def simulate_action(iam_client, role_arn: str, action: str) -> str:
    """
    Evaluate whether the role's attached policies allow an action.

    :param iam_client: Boto3 IAM client.
    :param role_arn: ARN of the IAM role to evaluate.
    :param action: IAM action name, e.g. ``ec2:DescribeTags``.
    :return: IAM evaluation decision: ``allowed``, ``implicitDeny``, or ``explicitDeny``.
    """
    response = iam_client.simulate_principal_policy(
        PolicySourceArn=role_arn,
        ActionNames=[action],
    )
    return response["EvaluationResults"][0]["EvalDecision"]


@pytest.mark.parametrize("aws_provider_version", ["~> 6.0"], ids=["aws-6"])
@pytest.mark.parametrize("profile_name", ["foo", "very-long-name" * 10])
def test_module(
    aws_provider_version,
    profile_name,
    aws_region,
    test_role_arn,
    keep_after,
    iam_client,
):
    terraform_module_dir = osp.join(TERRAFORM_ROOT_DIR, "instance-profile")

    # Delete .terraform.lock.hcl to allow provider version changes
    lock_file_path = osp.join(terraform_module_dir, ".terraform.lock.hcl")
    try:
        remove(lock_file_path)
    except FileNotFoundError:
        pass

    # Update the AWS provider version in terraform.tf
    terraform_tf_path = osp.join(terraform_module_dir, "terraform.tf")

    with open(terraform_tf_path, "w") as fp:
        fp.write(dedent(f"""
                terraform {{
                  required_providers {{
                    aws = {{
                      source  = "hashicorp/aws"
                      version = "{aws_provider_version}"
                    }}
                  }}
                }}
                """))

    with open(osp.join(terraform_module_dir, "terraform.tfvars"), "w") as fp:
        fp.write(dedent(f"""
                region       = "{aws_region}"
                profile_name = "{profile_name}"
                """))
        if test_role_arn:
            fp.write(dedent(f"""
                    role_arn     = "{test_role_arn}"
                    """))

    with terraform_apply(
        terraform_module_dir,
        destroy_after=not keep_after,
        json_output=True,
    ) as tf_output:
        LOG.info("%s", json.dumps(tf_output, indent=4))
        role_arn = tf_output["role_arn"]["value"]

        # The module grants ec2:DescribeTags by default (issue #30):
        # needed by the CloudWatch agent's ec2tagger and ASG lifecycle tooling.
        assert simulate_action(iam_client, role_arn, "ec2:DescribeTags") == "allowed"

        # Guard against over-granting: the module must not add permissions
        # beyond what the caller passed plus the documented defaults.
        assert (
            simulate_action(iam_client, role_arn, "ec2:DescribeVolumes")
            == "implicitDeny"
        )
