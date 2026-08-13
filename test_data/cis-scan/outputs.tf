output "account_id" {
  value = data.aws_caller_identity.this.account_id
}

output "instance_id" {
  value = aws_instance.scanned.id
}

output "role_arn" {
  value = module.profile.instance_role_arn
}

output "scan_target_tag_key" {
  value = "cis_scan_run"
}
