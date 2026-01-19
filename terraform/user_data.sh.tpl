#!/bin/bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y docker.io docker-compose-plugin git

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu || true

APP_DIR="/opt/recipe-app"
mkdir -p "${APP_DIR}"
cd "${APP_DIR}"

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

chown -R ubuntu:ubuntu "${APP_DIR}"
