output "mysql_ssh" {
  value = "ssh -i '${module.unique_name.unique}.pem' ec2-user@${module.mysql.ip_address}"
}