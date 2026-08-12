data "aws_iam_policy_document" "permissions" {
  statement {
    actions   = ["ec2:Describe*"]
    resources = ["*"]
  }
}

module "instance_profile" {
  source = "../../"

  profile_name = var.profile_name
  permissions  = data.aws_iam_policy_document.permissions.json

  # Attach existing managed policies in addition to the embedded one.
  extra_policies = {
    cloudwatch = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
  }

  tags = {
    environment = var.environment
  }
}
