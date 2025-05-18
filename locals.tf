locals {
  module_version = "1.6.2"

  default_module_tags = merge(
    var.tags,
    {
      created_by_module : "infrahouse/instance-profile/aws"
      upstream_module : var.upstream_module
    }
  )
}
