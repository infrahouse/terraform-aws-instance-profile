import json
from os import path as osp
from textwrap import dedent

import pytest
from infrahouse_toolkit.terraform import terraform_apply

from tests.conftest import (
    LOG,
    TRACE_TERRAFORM,
    DESTROY_AFTER,
    TEST_ROLE_ARN,
    REGION,
    TERRAFORM_ROOT_DIR,
)


@pytest.mark.parametrize("profile_name", ["foo", "very-long-name" * 10])
def test_module(profile_name):

    terraform_module_dir = osp.join(TERRAFORM_ROOT_DIR, "instance-profile")
    with open(osp.join(terraform_module_dir, "terraform.tfvars"), "w") as fp:
        fp.write(
            dedent(
                f"""
                region       = "{REGION}"
                role_arn     = "{TEST_ROLE_ARN}"
                profile_name = "{profile_name}"
                """
            )
        )

    with terraform_apply(
        terraform_module_dir,
        destroy_after=DESTROY_AFTER,
        json_output=True,
        enable_trace=TRACE_TERRAFORM,
    ) as tf_output:
        LOG.info("%s", json.dumps(tf_output, indent=4))
