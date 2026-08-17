# FastAPI 后端搭建模式（2026-07-03 实战总结）

## 项目结构（Domain-Driven）

```
backend/
├── app/
│   ├── main.py              # 应用工厂 + CORS + 路由注册
│   ├── config.py            # pydantic-settings 配置
│   ├── database.py          # Supabase 客户端
│   ├── api/v1/
│   │   ├── router.py        # 路由聚合
│   │   ├── generate.py      # AI 生成代理
│   │   ├── upload.py        # 文件上传
│   │   ├── credits.py       # 积分管理
│   │   └── stripe_routes.py # Stripe 接口
│   ├── schemas/             # Pydantic 请求/响应模型
│   └── services/            # 业务逻辑层
├── tests/
├── Dockerfile
└── requirements.txt
```

## Railway 部署要点

1. Dockerfile 必须使用 `${PORT:-8000}`（Railway 动态分配端口）
2. 环境变量通过 `railway variables set` 设置
3. 健康检查端点 `/health` 返回 `{"status": "healthy"}`

## toapis.com 代理模式

```python
async def proxy_toapis(endpoint: str, body: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://toapis.com/v1{endpoint}",
            json=body,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30.0
        )
        return response.json()
```

## Supabase 集成

```python
from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# 使用 service_role key 绕过 RLS
supabase_admin = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
```
