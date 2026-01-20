variable "aws_region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "us-east-1"
}

variable "project" {
  description = "Project name used for tagging."
  type        = string
  default     = "recipe-api"
}

variable "environment" {
  description = "Environment name used for tagging."
  type        = string
  default     = "prod"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.10.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet."
  type        = string
  default     = "10.10.1.0/24"
}

variable "instance_type" {
  description = "EC2 instance type for the app host."
  type        = string
  default     = "t3.micro"
}

variable "root_volume_size" {
  description = "Root volume size in GB for the EC2 instance."
  type        = number
  default     = 20
}

variable "ssh_key_name" {
  description = "Name of an existing AWS EC2 key pair for SSH access."
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed to SSH to the instance."
  type        = string
  default     = "0.0.0.0/0"
}

variable "django_secret_key" {
  description = "Django secret key passed to the container."
  type        = string
  sensitive   = true
}

variable "django_allowed_hosts" {
  description = "Comma-separated list of hosts allowed by Django."
  type        = string
}

variable "db_name" {
  description = "Postgres database name for the app."
  type        = string
  default     = "recipe"
}

variable "db_user" {
  description = "Postgres database user for the app."
  type        = string
  default     = "recipe"
}

variable "db_pass" {
  description = "Postgres database password for the app."
  type        = string
  sensitive   = true
}

variable "tags" {
  description = "Additional AWS resource tags."
  type        = map(string)
  default     = {}
}

variable "app_dir" {
  description = "Directory on the EC2 instance where the app code will be deployed."
  type        = string
  default     = "/opt/recipe-app"
}

variable "app_repo_url" {
  description = "Git repository URL containing the app source to deploy onto the EC2 instance."
  type        = string
  default     = "https://github.com/MaksimIleev/recipe-app-api"
}

variable "app_repo_ref" {
  description = "Optional git ref (branch, tag, or commit) to checkout after cloning."
  type        = string
  default     = ""
}
