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
  description = "Profile role name. If given, it will be used. Otherwise, the profile name will be used a name prefix."
  type        = string
  default     = null
}

variable "permissions" {
  description = "A JSON with a permissions policy. Note, a new policy will be created with these permissions."
}

variable "tags" {
  description = "A map of tags to add to resources."
  default     = {}
}

variable "upstream_module" {
  description = "Module that called this module."
  type        = string
  default     = null
}
