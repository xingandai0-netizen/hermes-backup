#!/bin/bash
# Antoken 部署脚本
# 使用方法: ./deploy.sh YOUR_SERVER_IP

set -e

if [ -z "$1" ]; then
  echo "使用方法: ./deploy.sh YOUR_SERVER_IP"
  exit 1
fi

SERVER_IP=$1
REMOTE_USER="root"
REMOTE_DIR="/opt/antoken"
WEB_DIR="/var/www/antoken"

echo "=== Antoken 部署脚本 ==="
echo "服务器: $SERVER_IP"
echo ""

# 1. 构建前端
echo ">>> 1. 构建前端..."
cd ~/antoken/frontend
npm run build
echo "前端构建完成"

# 2. 上传前端文件
echo ">>> 2. 上传前端文件..."
ssh $REMOTE_USER@$SERVER_IP "mkdir -p $WEB_DIR"
rsync -avz --delete out/ $REMOTE_USER@$SERVER_IP:$WEB_DIR/
echo "前端文件上传完成"

# 3. 上传后端文件
echo ">>> 3. 上传后端文件..."
ssh $REMOTE_USER@$SERVER_IP "mkdir -p $REMOTE_DIR/backend"
rsync -avz --delete \
  --exclude 'venv' \
  --exclude '__pycache__' \
  --exclude '.git' \
  ~/antoken/backend/ $REMOTE_USER@$SERVER_IP:$REMOTE_DIR/backend/
echo "后端文件上传完成"

# 4. 部署后端
echo ">>> 4. 部署后端..."
ssh $REMOTE_USER@$SERVER_IP << 'EOF'
cd /opt/antoken/backend

# 创建 Dockerfile（如果不存在）
if [ ! -f Dockerfile ]; then
  cat > Dockerfile << 'DOCKERFILE'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
DOCKERFILE
fi

# 创建 requirements.txt（如果不存在）
if [ ! -f requirements.txt ]; then
  cat > requirements.txt << 'REQ'
fastapi==0.109.0
uvicorn==0.27.0
httpx==0.26.0
python-multipart==0.0.6
REQ
fi

# 构建 Docker 镜像
docker build -t antoken-backend .

# 停止旧容器
docker stop antoken-backend 2>/dev/null || true
docker rm antoken-backend 2>/dev/null || true

# 启动新容器
docker run -d --name antoken-backend -p 8000:8000 --restart unless-stopped antoken-backend

echo "后端部署完成"
EOF

# 5. 重启 Nginx
echo ">>> 5. 重启 Nginx..."
ssh $REMOTE_USER@$SERVER_IP "nginx -t && systemctl restart nginx"
echo "Nginx 重启完成"

# 6. 验证部署
echo ">>> 6. 验证部署..."
sleep 3

# 检查前端
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://$SERVER_IP)
if [ "$HTTP_CODE" = "200" ]; then
  echo "✓ 前端正常 (HTTP $HTTP_CODE)"
else
  echo "✗ 前端异常 (HTTP $HTTP_CODE)"
fi

# 检查后端
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://$SERVER_IP:8000/docs)
if [ "$HTTP_CODE" = "200" ]; then
  echo "✓ 后端正常 (HTTP $HTTP_CODE)"
else
  echo "✗ 后端异常 (HTTP $HTTP_CODE)"
fi

echo ""
echo "=== 部署完成 ==="
echo "前端: http://$SERVER_IP"
echo "后端: http://$SERVER_IP:8000"
echo "工作空间: http://$SERVER_IP/workspace"
