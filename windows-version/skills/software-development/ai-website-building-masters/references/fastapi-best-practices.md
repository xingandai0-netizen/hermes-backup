# FastAPI 后端搭建最佳实践（2026-07-03 调研）

## 参考项目

| 项目 | Stars | 价值 |
|------|-------|------|
| zhanymkanov/fastapi-best-practices | 11,268 | 最佳实践指南 |
| ivan-borovets/fastapi-clean-example | 569 | Clean Architecture 模板 |
| wassim249/fastapi-langgraph-agent | 237 | AI Agent 后端模板 |

## 核心规则

### 1. 异步最佳实践
```python
# ❌ BAD: 阻塞事件循环
@router.get("/bad")
async def bad_endpoint():
    time.sleep(10)  # 阻塞所有请求

# ✅ GOOD: 同步路由在线程池运行
@router.get("/good")
def good_endpoint():
    time.sleep(10)  # 只阻塞这个线程

# ✅ PERFECT: 非阻塞 I/O
@router.get("/perfect")
async def perfect_endpoint():
    await asyncio.sleep(10)  # 非阻塞
```

### 2. CORS 配置
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://antokex.com"],  # 不要用 "*"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### 3. 错误处理
```python
class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

@app.exception_handler(AppException)
async def app_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
```

### 4. Pydantic v2 模型
```python
from pydantic import BaseModel, Field

class ImageGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    model: str = "gemini-3-pro-image-preview-official"
    size: str = Field(default="1:1", pattern=r"^\d+:\d+$")
```

### 5. Supabase 集成
```python
from supabase import create_client

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_supabase_admin() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
```

### 6. Stripe Webhook
```python
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    event = stripe.Webhook.construct_event(
        payload, sig_header, STRIPE_WEBHOOK_SECRET
    )
    
    if event["type"] == "checkout.session.completed":
        await handle_successful_payment(event["data"]["object"])
    
    return {"status": "ok"}
```

## 测试
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
```

## 部署（Railway）
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE ${PORT:-8000}
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```
