# Backend Security Patterns (2026-07-04)

## Global Exception Handler
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import traceback

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please contact support."}
    )
```

## SSRF Protection
```python
from urllib.parse import urlparse
import ipaddress

def is_safe_url(url: str) -> bool:
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        return False
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except ValueError:
        if hostname in ('localhost', '127.0.0.1', '0.0.0.0'):
            return False
    return True
```

## Config Validation at Startup
```python
class Settings(BaseSettings):
    def validate_required(self):
        missing = []
        if not self.SUPABASE_URL:
            missing.append("SUPABASE_URL")
        if not self.TOAPIS_API_KEY:
            missing.append("TOAPIS_API_KEY")
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# main.py startup event
@app.on_event("startup")
async def startup():
    settings.validate_required()
    get_supabase()  # Warm up connection
```

## Dynamic Credits Quota
```python
# Get user plan and calculate quota
profile = supabase.table("user_profiles").select("subscription_plan").eq("id", user_id).execute()
plan = "free"
if profile.data:
    plan = profile.data[0].get("subscription_plan", "free")

total_map = {
    "free": settings.FREE_CREDITS,
    "pro": settings.PRO_CREDITS,
    "business": settings.BUSINESS_CREDITS,
}
total = total_map.get(plan, settings.FREE_CREDITS)

# Pass to RPC
result = supabase.rpc("deduct_credits", {
    "p_user_id": request.user_id,
    "p_month": current_month,
    "p_amount": request.amount,
    "p_total": total,
}).execute()
```

## Error Detail Hiding
```python
# Wrong - leaks internal details
raise HTTPException(status_code=500, detail=str(e))

# Right - log details, return generic message
logger.error(f"Upload error: {e}", exc_info=True)
raise HTTPException(status_code=500, detail="File upload failed, please try again.")
```

## Replace print with logger
```python
# Wrong
print(f"Checkout completed: user={user_id}")

# Right
logger.info(f"Checkout completed: user={user_id}")
```

## Pydantic Model Validation
```python
# Wrong - direct JSON parsing
body = await request.json()
user_id = body.get("user_id")

# Right - Pydantic model
class CancelSubscriptionRequest(BaseModel):
    user_id: str = Field(..., min_length=36, max_length=36, pattern=r'^[a-f0-9-]+$')

async def cancel_subscription(request: CancelSubscriptionRequest):
    # request.user_id is validated
```
