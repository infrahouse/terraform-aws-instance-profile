output "instance_profile_name" {
  description = "Instance profile name. It's the same as the passed variable."
  value       = aws_iam_instance_profile.profile.name
}

output "instance_profile_arn" {
  description = "Instance profile ARN."
  value       = aws_iam_instance_profile.profile.arn
}

output "instance_role_name" {
  description = "Role name that the instance gets."
  value       = aws_iam_role.profile.name
}

output "instance_role_arn" {
  description = "Role ARN that the instance gets."
  value       = aws_iam_role.profile.arn
}
