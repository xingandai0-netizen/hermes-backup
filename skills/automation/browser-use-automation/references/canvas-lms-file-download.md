# Canvas LMS 文件下载技术笔记

## 背景
Canvas (Instructure) 是常见的教育LMS平台。本session需要从Canvas下载docx文件，但curl直接下载只能获取登录页面(HTML)，说明需要携带有效session cookie。

## 关键发现

### 1. Canvas API 文件元信息端点
```
GET /api/v1/courses/{course_id}/files/{file_id}
```
返回JSON，包含:
- `size`: 文件大小(bytes)
- `url`: `https://stanfort.instructure.com/files/{file_id}/download?download_frd=1`
- `content-type`: MIME类型
- `display_name`: 显示文件名

### 2. 下载URL格式
```
https://stanfort.instructure.com/files/{file_id}/download?download_frd=1
```
`download_frd=1` 参数表示强制下载。

### 3. 认证机制
- Canvas使用session cookie认证（`_csrf_token`）
- curl不带cookie下载只能得到登录页面
- 浏览器已登录状态可以正常下载

## 解决方案尝试

### 方法A: 浏览器控制台下载
```javascript
fetch('/courses/{course_id}/files/{file_id}/download', {credentials: 'same-origin'})
  .then(r => r.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'filename.docx';
    a.click();
  });
```
**结果**: `Failed to fetch` - 浏览器安全限制阻止跨域fetch

### 方法B: 从API获取下载链接后用curl
1. 调用API获取元信息(含下载URL)
2. curl携带cookie访问下载URL

**问题**: curl无法直接获取浏览器session cookie（安全隔离）

### 方法C: 直接点击下载链接（当前方案）
浏览器已登录时，直接访问文件页面，点击下载链接即可。

## Canvas文件页面结构
```
URL: /courses/{course_id}/files/{file_id}?module_item_id={item_id}
关键元素:
- 下载链接: link "Download {filename}"
- 预览iframe: iframe "File preview for {filename}" (可能403)
```

## 课程ID和文件ID
- 课程ID: 966
- 文件ID: 208781
- 完整URL: https://stanfort.instructure.com/courses/966/files/208781

## 通用模式
1. 登录Canvas（邮箱+密码）
2. 导航到课程文件页面
3. 点击下载链接或使用API获取真实下载URL
4. 下载文件到本地

## 待解决
如何从浏览器导出session cookie给curl（跨进程共享cookie）
可能的方案: 使用browser-use的cookie提取功能，或者DrissionPage的cookie同步