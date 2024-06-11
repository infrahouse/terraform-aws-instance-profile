resource "aws_iam_policy" "profile" {
  name_prefix = var.profile_name
  policy      = var.permissions
  tags        = local.tags
}

resource "aws_iam_role" "profile" {
  name               = var.role_name != null ? var.role_name : null
  name_prefix        = var.role_name == null ? var.profile_name : null
  assume_role_policy = data.aws_iam_policy_document.assume.json
  tags               = local.tags
}

resource "aws_iam_role_policy_attachment" "profile" {
  policy_arn = aws_iam_policy.profile.arn
  role       = aws_iam_role.profile.name
}

resource "aws_iam_instance_profile" "profile" {
  name = var.profile_name
  role = aws_iam_role.profile.name
  tags = local.tags
}

resource "aws_iam_role_policy_attachment" "extra" {
  for_each   = var.extra_policies
  policy_arn = each.value
  role       = aws_iam_role.profile.name
}
