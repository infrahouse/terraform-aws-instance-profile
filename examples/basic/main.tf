data "aws_iam_policy_document" "permissions" {
  statement {
    actions   = ["ec2:Describe*"]
    resources = ["*"]
  }
}

module "instance_profile" {
  source  = "registry.infrahouse.com/infrahouse/instance-profile/aws"
  version = "2.0.0"

  profile_name = var.profile_name
  permissions  = data.aws_iam_policy_document.permissions.json

  tags = {
    environment = var.environment
  }
}
