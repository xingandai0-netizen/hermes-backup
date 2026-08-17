---
name: certbot-ssl-management
description: 使用certbot管理SSL证书，自动配置HTTPS
version: 1.0.0
author: Hermes Agent
---

# Certbot SSL证书管理

## 核心功能

### 证书申请
- 自动从Let's Encrypt申请免费证书
- 支持多种验证方式
- 自动续期

### 证书管理
- 安装证书
- 更新证书
- 吊销证书
- 查看证书状态

## 基础用法

### 安装Certbot
```bash
# Ubuntu/Debian
sudo apt install certbot

# CentOS/RHEL
sudo yum install certbot

# macOS
brew install certbot

# Python方式
pip install certbot
```

### 申请证书
```bash
# Nginx插件
sudo certbot --nginx -d example.com -d www.example.com

# Apache插件
sudo certbot --apache -d example.com -d www.example.com

# 手动验证
sudo certbot certonly --manual -d example.com
```

### 查看证书
```bash
# 查看证书列表
sudo certbot certificates

# 查看证书详情
sudo openssl x509 -in /etc/letsencrypt/live/example.com/cert.pem -text -noout
```

## 自动续期

### 设置定时任务
```bash
# 编辑crontab
sudo crontab -e

# 添加定时任务（每天凌晨2点检查）
0 2 * * * certbot renew --quiet
```

### Systemd定时器
```bash
# 创建timer文件
sudo nano /etc/systemd/system/certbot.timer

[Unit]
Description=Certbot SSL renewal

[Timer]
OnCalendar=*-*-* 02:00:00
RandomizedDelaySec=1hour
Persistent=true

[Install]
WantedBy=timers.target

# 启用timer
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Nginx配置

### 自动配置
```bash
sudo certbot --nginx -d example.com
```

### 手动配置
```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # SSL优化配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # 其他配置...
}
```

## 高级功能

### 使用DNS验证
```bash
# 使用Cloudflare DNS验证
sudo certbot certonly   --dns-cloudflare   --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini   -d example.com   -d *.example.com
```

### 通配符证书
```bash
# 申请通配符证书
sudo certbot certonly   --manual --preferred-challenges dns   -d *.example.com   -d example.com
```

### 重载服务
```bash
# 重载Nginx
sudo systemctl reload nginx

# 重载Apache
sudo systemctl reload apache2

# 自动重载（在renewal hook中）
sudo nano /etc/letsencrypt/renewal-hooks/post/nginx-reload.sh
#!/bin/bash
systemctl reload nginx
```

## 证书管理

### 手动续期
```bash
# 续期所有证书
sudo certbot renew

# 续期特定证书
sudo certbot renew --cert-name example.com

# 测试续期（不实际续期）
sudo certbot renew --dry-run
```

### 吊销证书
```bash
# 吊销证书
sudo certbot revoke --cert-path /etc/letsencrypt/live/example.com/cert.pem

# 删除证书
sudo certbot delete --cert-name example.com
```

### 查看日志
```bash
# 查看certbot日志
sudo journalctl -u certbot

# 查看详细日志
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

## 多域名管理

### 单证书多域名
```bash
sudo certbot --nginx   -d example.com   -d www.example.com   -d api.example.com   -d admin.example.com
```

### 独立证书
```bash
# 为每个子域名单独申请
sudo certbot --nginx -d example.com
sudo certbot --nginx -d api.example.com
sudo certbot --nginx -d admin.example.com
```

## 故障排除

### 常见错误

#### 验证失败
```bash
# 检查DNS解析
dig example.com

# 检查80端口是否开放
sudo netstat -tulpn | grep :80

# 手动验证文件
sudo python -m http.server 80 --directory /var/www/html
```

#### 证书过期
```bash
# 强制续期
sudo certbot renew --force-renewal

# 检查到期时间
sudo openssl x509 -in /etc/letsencrypt/live/example.com/cert.pem -noout -dates
```

#### 权限问题
```bash
# 修复权限
sudo chown -R root:root /etc/letsencrypt
sudo chmod -R 700 /etc/letsencrypt
```

## 最佳实践

1. **自动续期**: 设置定时任务自动续期
2. **监控到期**: 监控证书到期时间
3. **备份证书**: 定期备份证书文件
4. **测试环境**: 先在测试环境验证
5. **日志记录**: 记录所有证书操作

## API使用

### Python API
```python
import subprocess

def renew_certificates():
    """续期证书"""
    result = subprocess.run(
        ["sudo", "certbot", "renew"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def check_certificate(domain):
    """检查证书状态"""
    result = subprocess.run(
        ["sudo", "certbot", "certificates", "-d", domain],
        capture_output=True,
        text=True
    )
    return result.stdout
```

## 与传统方式对比

| 特性 | Certbot | 手动配置 |
|------|---------|---------|
| 证书申请 | 自动 | 手动 |
| 续期 | 自动 | 手动 |
| 成本 | 免费 | 可能收费 |
| 安全性 | 高 | 取决于操作 |
| 维护 | 低 | 高 |
