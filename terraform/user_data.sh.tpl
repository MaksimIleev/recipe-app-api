#!/bin/bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y ca-certificates curl gnupg git

# Install Docker from the official Docker apt repo to ensure compose plugin is available
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
  | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu || true

APP_DIR="${APP_DIR}"
APP_REPO_URL="${app_repo_url}"
APP_REPO_REF="${app_repo_ref}"

mkdir -p "$(dirname "$APP_DIR")"
rm -rf "$APP_DIR"
git clone "$APP_REPO_URL" "$APP_DIR"
if [ -n "$APP_REPO_REF" ]; then
  git -C "$APP_DIR" checkout "$APP_REPO_REF"
fi

cd "$APP_DIR"

cat > .env <<'EOF'
DJANGO_SECRET_KEY=${django_secret_key}
DJANGO_ALLOWED_HOSTS=${allowed_hosts}
DB_HOST=db
DB_NAME=${db_name}
DB_USER=${db_user}
DB_PASS=${db_pass}
DEBUG=0
EOF

cat > docker-compose.yml <<'EOF'
${docker_compose}
EOF

docker compose -f docker-compose.yml pull || true
docker compose -f docker-compose.yml up -d --build

chown -R ubuntu:ubuntu "$APP_DIR"
