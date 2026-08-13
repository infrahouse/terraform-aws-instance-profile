data "aws_caller_identity" "this" {}

data "aws_subnet" "selected" {
  id = var.subnet_id
}

# Ubuntu 22.04 LTS — in Amazon Inspector's supported OS list for CIS scans,
# ships with the SSM agent preinstalled.
data "aws_ssm_parameter" "ubuntu_ami" {
  name = "/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id"
}

# Minimal harmless permissions - the module requires the input,
# but this test only cares about the permissions the module adds on its own.
data "aws_iam_policy_document" "permissions" {
  statement {
    actions = [
      "sts:GetCallerIdentity"
    ]
    resources = [
      "*"
    ]
  }
}
