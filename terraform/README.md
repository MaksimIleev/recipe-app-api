# Terraform deployment to EC2

This configuration provisions a minimal public subnet, security group, Elastic IP, and an Ubuntu EC2 host that boots the existing `docker-compose-deploy.yml` stack with your supplied environment values.

## Prerequisites
- Terraform >= 1.5, AWS credentials with permissions for VPC/EC2/EIP.
- An existing EC2 key pair (`ssh_key_name` variable).
- A Git URL the instance can clone at boot (`app_repo_url`); optionally set `app_repo_ref` to pin a branch/tag/commit. Public HTTPS is simplest; for private repos use a deploy token/credential helper.
- Values for `django_secret_key`, `django_allowed_hosts` (include your domain/IP), and `db_pass`.

## Usage
```bash
cd terraform
terraform init
terraform plan \
  -var 'ssh_key_name=<your-keypair>' \
  -var 'app_repo_url=<https-git-url>' \
  -var 'django_secret_key=<secret>' \
  -var 'django_allowed_hosts=<domain-or-ip>' \
  -var 'db_pass=<db-password>'
terraform apply  # confirm plan
```

Outputs include the Elastic IP, app URL, and SSH command. Update `allowed_ssh_cidr` from the default `0.0.0.0/0` to your IP before applying.

## What gets created
- New VPC with one public subnet and Internet gateway.
- Security group allowing HTTP/HTTPS and SSH (CIDR-controlled).
- Ubuntu EC2 instance with Docker + compose installed via cloud-init, running `docker compose up -d --build`.
- Elastic IP attached to the instance.

## Post-deploy
- SSH to the host and run migrations when needed:
  ```bash
  ssh ubuntu@<elastic-ip>
  cd /opt/recipe-app
  docker compose -f docker-compose.yml exec app python manage.py migrate
  ```
- To tear down everything: `terraform destroy`.

## Notes
- Secrets set via variables are stored in Terraform state; use a secured backend (e.g., S3 with encryption) and restrict access.
- Root volume defaults to 20GB and instance type to `t3.micro`; adjust via variables for production workloads.
