output "app_public_ip" {
  description = "Elastic IP for the app host."
  value       = aws_eip.app.public_ip
}

output "app_url" {
  description = "HTTP endpoint for the app once containers are up."
  value       = "http://${aws_eip.app.public_ip}"
}

output "ssh_command" {
  description = "Convenience SSH command (replace with your private key path)."
  value       = "ssh ubuntu@${aws_eip.app.public_ip}"
}

output "instance_id" {
  description = "ID of the EC2 instance running the app."
  value       = aws_instance.app.id
}
