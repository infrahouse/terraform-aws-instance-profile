module "profile" {
  source       = "../../"
  permissions  = data.aws_iam_policy_document.permissions.json
  profile_name = "cis-scan-${var.run_id}"
}

# No ingress: the SSM agent only needs an outbound path to the SSM endpoints.
resource "aws_security_group" "scanned" {
  name_prefix = "cis-scan-${var.run_id}"
  description = "Egress-only security group for the CIS scan test instance"
  vpc_id      = data.aws_subnet.selected.vpc_id
}

resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.scanned.id
  description       = "Allow all egress (SSM, package mirrors)"
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_instance" "scanned" {
  ami                         = nonsensitive(data.aws_ssm_parameter.ubuntu_ami.value)
  instance_type               = "t3.micro"
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.scanned.id]
  associate_public_ip_address = true
  iam_instance_profile        = module.profile.instance_profile_name

  metadata_options {
    http_tokens = "required"
  }

  root_block_device {
    encrypted   = true
    volume_type = "gp3"
  }

  tags = {
    Name = "cis-scan-${var.run_id}"
    # Inspector CIS scan configurations target instances by tag.
    cis_scan_run = var.run_id
  }
}
