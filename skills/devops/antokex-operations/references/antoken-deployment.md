# Antoken 部署到 antokex 服务器

## 架构

```
Internet → Cloudflare → Nginx → antoken.antokex.com
                            ├── / → 着陆页（静态 HTML）
                            ├── /workspace → 工作流编辑器（静态 HTML）
                            └── /api/* → FastAPI 后端 (localhost:8000)
```

## 部署步骤

### 1. 前端构建

```bash
cd ~/antoken/frontend
npm run build  # 输出到 out/ 目录
```

### 2. 上传到服务器

```bash
rsync -avz out/ root@SERVER_IP:/var/www/antoken/
```

### 3. 后端部署

```bash
# 上传代码
rsync -avz ~/antoken/backend/ root@SERVER_IP:/opt/antoken/backend/

# Docker 构建
cd /opt/antoken/backend
docker build -t antoken-backend .
docker run -d --name antoken-backend -p 8000:8000 --restart unless-stopped antoken-backend
```

### 4. Nginx 配置

```nginx
server {
    listen 80;
    server_name antoken.antokex.com;

    root /var/www/antoken;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
    }
}
```

### 5. SSL 证书

```bash
certbot --nginx -d antoken.antokex.com
```

## 与 antokex 共存

- antoken 使用子域名 `antoken.antokex.com`
- 共享同一台服务器
- Nginx 配置独立，互不影响
- 后端 Docker 容器独立运行
