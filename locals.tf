locals {
  module_version = "2.0.0"

  default_module_tags = merge(
    var.tags,
    {
      created_by_module : "infrahouse/instance-profile/aws"
      upstream_module : var.upstream_module
    }
  )
}
