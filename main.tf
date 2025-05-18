resource "aws_iam_policy" "profile" {
  # expected length of name_prefix to be in the range (1 - 102)
  name_prefix = substr(var.profile_name, 0, 102)
  policy      = var.permissions
  tags        = local.default_module_tags
}

resource "aws_iam_role" "profile" {
  name = var.role_name != null ? var.role_name : null
  # expected length of name_prefix to be in the range (1 - 38)
  name_prefix        = var.role_name == null ? substr(var.profile_name, 0, 38) : null
  assume_role_policy = data.aws_iam_policy_document.assume.json
  tags = merge(
    {
      module_version = local.module_version
    },
    local.default_module_tags
  )
}

resource "aws_iam_role_policy_attachment" "profile" {
  policy_arn = aws_iam_policy.profile.arn
  role       = aws_iam_role.profile.name
}

resource "aws_iam_instance_profile" "profile" {
  # expected length of name to be in the range (1 - 128)
  name = substr(var.profile_name, 0, 128)
  role = aws_iam_role.profile.name
  tags = local.default_module_tags
}

resource "aws_iam_role_policy_attachment" "extra" {
  for_each   = var.extra_policies
  policy_arn = each.value
  role       = aws_iam_role.profile.name
}
