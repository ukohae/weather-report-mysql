module "mysql" {
  source          = "git::https://github.com/devops-terraform-aws/ec2-instance-module.git?ref=v1.0.0"
  ami             = data.aws_ami.redhat-linux.id
  key_name        = module.aws_key.get_key_name
  instance_type   = var.instance_type
  name            = "mysql-${var.name}-${module.unique_name.unique}"
  user_data       = file("${path.module}/scripts/mysql.sh")
  security_groups = module.security_group.security_name
  region          = var.region
}

module "security_group" {
  source      = "git::https://github.com/devops-terraform-aws/security-group-module.git?ref=v1.0.0"
  name        = "${local.name}-${module.unique_name.unique}"
  cidr_blocks = ["${chomp(data.http.myip.response_body)}/32"]
}

module "unique_name" {
  source = "git::https://github.com/devops-terraform-aws/random-module.git?ref=v1.0.0"
}

module "aws_key" {
  source   = "git::https://github.com/devops-terraform-aws/ssh-key-module.git?ref=v1.0.0"
  key_name = module.unique_name.unique
}

resource "terraform_data" "generated_key" {
  provisioner "local-exec" {
    command = <<-EOT
        echo '${module.aws_key.private_key}' > ./'${module.unique_name.unique}'.pem
        chmod 400 ./'${module.unique_name.unique}'.pem
      EOT
  }
}


resource "terraform_data" "copy_script" {
  provisioner "file" {
    source      = "scripts/weather.py"
    destination = "weather.py"
  }

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file("${module.unique_name.unique}.pem")
    host        = module.mysql.ip_address
  }
  depends_on = [terraform_data.generated_key]
}