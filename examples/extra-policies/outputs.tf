output "instance_profile_arn" {
  description = "Instance profile ARN."
  value       = module.instance_profile.instance_profile_arn
}

output "instance_profile_name" {
  description = "Instance profile name."
  value       = module.instance_profile.instance_profile_name
}

output "instance_role_arn" {
  description = "Role ARN that the instance gets."
  value       = module.instance_profile.instance_role_arn
}
