import json
from os import path as osp
from textwrap import dedent

import pytest
from pytest_infrahouse import terraform_apply

from tests.conftest import (
    LOG,
    TERRAFORM_ROOT_DIR,
)


@pytest.mark.parametrize("profile_name", ["foo", "very-long-name" * 10])
def test_module(profile_name, aws_region, test_role_arn, keep_after):
    terraform_module_dir = osp.join(TERRAFORM_ROOT_DIR, "instance-profile")
    with open(osp.join(terraform_module_dir, "terraform.tfvars"), "w") as fp:
        fp.write(
            dedent(
                f"""
                region       = "{aws_region}"
                role_arn     = "{test_role_arn}"
                profile_name = "{profile_name}"
                """
            )
        )

    with terraform_apply(
        terraform_module_dir,
        destroy_after=not keep_after,
        json_output=True,
    ) as tf_output:
        LOG.info("%s", json.dumps(tf_output, indent=4))
