locals {
  tags = merge(
    var.tags,
    {
      created_by_module : "infrahouse/instance-profile/aws"
      upstream_module : var.upstream_module
    }
  )
}
