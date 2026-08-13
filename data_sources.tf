data "aws_iam_policy_document" "assume" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy" "ssm" {
  name = "AmazonSSMManagedInstanceCore"
}

# Caller-supplied permissions merged with defaults every EC2 instance needs.
#
# ec2:DescribeTags is granted by default because standard instance tooling
# depends on it: the CloudWatch agent's ec2tagger reads the
# aws:autoscaling:groupName tag to populate the AutoScalingGroupName metric
# dimension, and ASG lifecycle tooling discovers the instance's own ASG the
# same way. The action is read-only and does not support resource-level
# permissions (AWS API limitation), so it must be granted on "*".
# https://github.com/infrahouse/terraform-aws-instance-profile/issues/30
data "aws_iam_policy_document" "permissions" {
  source_policy_documents = [var.permissions]

  statement {
    actions   = ["ec2:DescribeTags"]
    resources = ["*"]
  }

  # Amazon Inspector CIS benchmark scans: the Inspector SSM plugin uses the
  # instance profile credentials to open a CIS session directly against the
  # regional Inspector endpoint. Without these actions the session gets a 403
  # and the scan silently times out reporting zero checks. Verified by
  # tests/test_cis_e2e.py. Resource "*" per the AWS prerequisites:
  # https://docs.aws.amazon.com/inspector/latest/user/scanning-cis.html
  # https://github.com/infrahouse/terraform-aws-instance-profile/issues/33
  statement {
    actions = [
      "inspector2:StartCisSession",
      "inspector2:StopCisSession",
      "inspector2:SendCisSessionTelemetry",
      "inspector2:SendCisSessionHealth",
    ]
    resources = ["*"]
  }
}
