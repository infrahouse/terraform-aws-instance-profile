variable "region" {}
variable "role_arn" {
  default = null
}
variable "run_id" {
  description = "Unique identifier of the test run; used in resource names and the scan target tag."
}
variable "subnet_id" {
  description = "Public subnet to launch the scanned instance in (SSM needs an outbound path)."
}
