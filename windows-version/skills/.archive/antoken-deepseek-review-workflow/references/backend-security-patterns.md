# 后端安全模式参考

## 全局异常处理器

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(status_code=500, content={"detail": "Internal server error."})
```

## 配置校验

```python
def validate_required(self):
    missing = []
    if not self.SUPABASE_URL: missing.append("SUPABASE_URL")
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
```

## SSRF 防护

```python
def is_safe_url(url: str) -> bool:
    parsed = urlparse(url)
    hostname = parsed.hostname
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except ValueError:
        if hostname in ('localhost', '127.0.0.1', '0.0.0.0'):
            return False
    return True
```

## 积分动态配额

```python
profile = supabase.table("user_profiles").select("subscription_plan").eq("id", user_id).execute()
plan = profile.data[0].get("subscription_plan", "free")
total_map = {"free": 100, "pro": 1000, "business": 5000}
total = total_map.get(plan, 100)
```

## toapis.com API 格式

### 文本生成（OpenAI 兼容格式）
```python
body = {"messages": [{"role": "user", "content": "..."}], "model": "gemini-3.5-flash"}
```

### 图片/视频生成
```python
body = {"prompt": "...", "model": "...", "size": "1:1", "resolution": "2K"}
```

## 图片预览优化（Pillow 缩放）

```python
@router.get("/generate/proxy")
async def proxy_media(url: str, width: int = None, height: int = None):
    if width and height and content_type.startswith("image/"):
        cache_key = hashlib.md5(f"{url}_{width}_{height}".encode()).hexdigest()
        # 缩放并缓存
```
