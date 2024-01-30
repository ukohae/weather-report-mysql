data "aws_ami" "redhat-linux" {
  most_recent = true

  filter {
    name   = "name"
    values = ["RHEL-8.6.0_HVM-20220503-x86_64-*"]
  }
}

data "http" "myip" {
  url = "http://ipv4.icanhazip.com"
}