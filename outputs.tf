output "jenkins_ssh" {
  value = "ssh -i '${module.unique_name.unique}.pem' ubuntu@${module.jenkins.ip_address}"
}

output "jenkins_browser" {
  value = "${module.jenkins.ip_address}:8080"
}