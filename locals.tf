locals {
  tags = merge(
    {
      created_by_module : "infrahouse/instance-profile/aws"
      upstream_module : var.upstream_module
    },
    var.tags
  )
}
