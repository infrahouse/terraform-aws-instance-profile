variable "enable_ssm" {
  description = "Add AmazonSSMManagedInstanceCore policy to the instance role to grant an EC2 instance the minimum set of permissions needed to use AWS Systems Manager (SSM) core functionality."
  type        = bool
  default     = true
}

variable "extra_policies" {
  description = "A map of additional policy ARNs to attach to the instance role"
  type        = map(string)
  default     = {}
}

variable "profile_name" {
  description = "Instance profile name."
  type        = string
}

variable "role_name" {
  description = "Profile role name. If given, it will be used. Otherwise, the profile name will be used as a name prefix."
  type        = string
  default     = null
}

variable "permissions" {
  description = <<-EOT
    A JSON with a permissions policy. Note, a new policy will be created with these permissions.
    The module adds ec2:DescribeTags to the given permissions - the CloudWatch agent
    and Auto Scaling lifecycle tooling need it, and it cannot be scoped to a resource.
  EOT
  type        = string
}

variable "tags" {
  description = "A map of tags to add to resources."
  type        = map(string)
  default     = {}
}

variable "upstream_module" {
  description = "Module that called this module."
  type        = string
  default     = null
}
