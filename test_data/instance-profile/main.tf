module "profile" {
  source       = "../../"
  permissions  = data.aws_iam_policy_document.permissions.json
  profile_name = var.profile_name
}
