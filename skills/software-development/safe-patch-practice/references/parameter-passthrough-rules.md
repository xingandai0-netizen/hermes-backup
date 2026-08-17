# 参数透传规则

## 核心原则
用户设置的每个参数都必须 100% 传递到 AI API，中间不得有任何截断。

## 常见断裂点

### 1. 字段名不匹配
```python
# ❌ 前端发送 ratio，后端期望 aspect_ratio
body = {"ratio": request.ratio}  # API 不认

# ✅ 后端做映射
body = {"aspect_ratio": request.ratio}
```

### 2. Schema 缺失字段
```python
# ❌ 前端发送 video_mode，后端 Schema 未定义
# Pydantic 会静默丢弃未定义的字段

# ✅ 在 Schema 中添加字段
class VideoGenerateRequest(BaseModel):
    video_mode: Optional[str] = None
```

### 3. 参数位置错误
```python
# ❌ resolution 包装在 metadata 中
body = {"metadata": {"resolution": "2K"}}  # API 不认

# ✅ resolution 作为顶层字段
body = {"resolution": "2K"}
```

### 4. 参考数据丢失
```python
# ❌ 前端发送 reference_images，后端未定义
# Pydantic 静默丢弃

# ✅ 在 Schema 中添加
class ImageGenerateRequest(BaseModel):
    reference_images: Optional[List[ReferenceImage]] = None
```

## 验证清单
- [ ] 前端发送的每个字段都有对应的后端 Schema 定义
- [ ] 字段名一致或后端做映射
- [ ] 参数位置正确（顶层 vs 嵌套）
- [ ] 参考数据结构完整（url + role + name）

## toapis.com API 参数格式

### 图片生成
```json
{
  "prompt": "...",
  "model": "gemini-3-pro-image-preview-official",
  "size": "1:1",
  "resolution": "2K",
  "reference_images": [
    {"url": "https://...", "role": "style"},
    {"url": "https://...", "role": "subject"}
  ]
}
```

### 视频生成
```json
{
  "prompt": "...",
  "model": "seedance-2",
  "aspect_ratio": "9:16",
  "resolution": "720p",
  "duration": 5,
  "video_mode": "first_frame",
  "first_frame_url": "https://...",
  "reference_images": [{"url": "https://...", "role": "style"}]
}
```

### 文本生成（OpenAI 兼容格式）
```json
{
  "messages": [{"role": "user", "content": "..."}],
  "model": "gemini-3.5-flash"
}
```
注意：不是 `{"prompt": "..."}`，必须用 `messages` 数组。
