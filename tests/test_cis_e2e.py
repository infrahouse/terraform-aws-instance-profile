"""
End-to-end sufficiency test for Amazon Inspector CIS scans (issue #33).

The tier-1 assertions in test_module.py prove the module grants the
permissions it promises. This test proves those permissions are enough:
a real CIS benchmark scan against a real instance wearing the module's
profile must complete with checks, instead of silently timing out with
zero checks (the failure mode described in the issue).

Slow (~15-30 minutes) and ad-hoc: runs only with --run-cis-e2e,
via ``make test-cis``.
"""

import uuid
from os import path as osp
from textwrap import dedent
from time import sleep
from typing import Any, Dict

import pytest
from infrahouse_core.aws.ec2_instance import EC2Instance
from infrahouse_core.timeout import timeout
from pytest_infrahouse import terraform_apply

from tests.conftest import (
    LOG,
    TERRAFORM_ROOT_DIR,
)

SSM_SEND_TIMEOUT = 15 * 60
SCAN_TIMEOUT = 45 * 60
POLL_INTERVAL = 30


def wait_for_scan_target_result(
    inspector2_client, scan_configuration_arn: str, instance_id: str
) -> Dict[str, Any]:
    """
    Block until the CIS scan triggered by the configuration reports a terminal
    result for the instance, and return that target aggregation.

    :param inspector2_client: Boto3 Inspector2 client.
    :param scan_configuration_arn: ARN of the CIS scan configuration.
    :param instance_id: EC2 instance id the scan targets.
    :return: Target resource aggregation with ``targetStatus``,
        ``targetStatusReason``, and ``statusCounts``.
    :raise TimeoutError: if no terminal target result appears within SCAN_TIMEOUT.
    """
    with timeout(SCAN_TIMEOUT):
        while True:
            scans = inspector2_client.list_cis_scans(
                filterCriteria={
                    "scanConfigurationArnFilters": [
                        {"comparison": "EQUALS", "value": scan_configuration_arn}
                    ]
                }
            )["scans"]
            for scan in scans:
                aggregations = inspector2_client.list_cis_scan_results_aggregated_by_target_resource(
                    scanArn=scan["scanArn"]
                )[
                    "targetResourceAggregations"
                ]
                targets = [
                    target
                    for target in aggregations
                    if target["targetResourceId"] == instance_id
                ]
                if targets:
                    target = targets[0]
                    LOG.info(
                        "Scan status: %s, target status: %s, reason: %s",
                        scan["status"],
                        target.get("targetStatus"),
                        target.get("targetStatusReason"),
                    )
                    if target.get("targetStatus") in (
                        "COMPLETED",
                        "TIMED_OUT",
                        "CANCELLED",
                    ):
                        return target
                else:
                    LOG.info("Scan status: %s, target not reported yet", scan["status"])
            LOG.info("Waiting for CIS scan result...")
            sleep(POLL_INTERVAL)


@pytest.mark.cis_e2e
def test_cis_scan_completes(
    service_network,
    aws_region,
    test_role_arn,
    keep_after,
    boto3_session,
):
    run_id = uuid.uuid4().hex[:12]
    subnet_id = service_network["subnet_public_ids"]["value"][0]
    terraform_module_dir = osp.join(TERRAFORM_ROOT_DIR, "cis-scan")

    with open(osp.join(terraform_module_dir, "terraform.tfvars"), "w") as fp:
        fp.write(dedent(f"""
                region    = "{aws_region}"
                run_id    = "{run_id}"
                subnet_id = "{subnet_id}"
                """))
        if test_role_arn:
            # keep terraform fmt happy: align '=' with the block above
            fp.write(f'role_arn  = "{test_role_arn}"\n')

    with terraform_apply(
        terraform_module_dir,
        destroy_after=not keep_after,
        json_output=True,
    ) as tf_output:
        instance_id = tf_output["instance_id"]["value"]
        account_id = tf_output["account_id"]["value"]
        tag_key = tf_output["scan_target_tag_key"]["value"]

        # Inspector CIS scans require the target to be an online SSM managed
        # node. execute_command() waits for the SSM agent to respond, proving
        # the instance is scannable before the scan configuration is created.
        instance = EC2Instance(
            instance_id=instance_id, region=aws_region, session=boto3_session
        )
        ret, stdout, stderr = instance.execute_command(
            "uname -a", send_timeout=SSM_SEND_TIMEOUT
        )
        assert ret == 0, f"SSM command failed: {stderr}"
        LOG.info("Instance %s is SSM-managed: %s", instance_id, stdout.strip())

        inspector2_client = boto3_session.client("inspector2")
        scan_configuration_arn = inspector2_client.create_cis_scan_configuration(
            scanName=f"cis-e2e-{run_id}",
            securityLevel="LEVEL_1",
            schedule={"oneTime": {}},
            targets={
                "accountIds": [account_id],
                "targetResourceTags": {tag_key: [run_id]},
            },
        )["scanConfigurationArn"]
        LOG.info("Created one-time CIS scan configuration %s", scan_configuration_arn)

        try:
            target = wait_for_scan_target_result(
                inspector2_client, scan_configuration_arn, instance_id
            )

            # Sufficiency: the scan must actually complete with checks.
            # Without the inspector2 CIS session permissions on the instance
            # role, the target times out and reports zero checks (issue #33).
            assert target["targetStatus"] == "COMPLETED", (
                f"CIS scan did not complete for {instance_id}: "
                f"status {target['targetStatus']}, "
                f"reason {target.get('targetStatusReason')}"
            )
            checks = sum(target.get("statusCounts", {}).values())
            assert checks > 0, f"CIS scan completed but reported no checks: {target}"
            LOG.info("CIS scan completed with %d checks: %s", checks, target)
        finally:
            inspector2_client.delete_cis_scan_configuration(
                scanConfigurationArn=scan_configuration_arn
            )
            LOG.info("Deleted CIS scan configuration %s", scan_configuration_arn)
