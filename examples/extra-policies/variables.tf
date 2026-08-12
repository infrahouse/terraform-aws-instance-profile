variable "environment" {
  type        = string
  description = "Environment name (development, staging, production, etc.)"
}

variable "profile_name" {
  type        = string
  description = "Instance profile name."
  default     = "extra-policies-example"
}

variable "region" {
  type        = string
  description = "AWS region to create resources in."
}
