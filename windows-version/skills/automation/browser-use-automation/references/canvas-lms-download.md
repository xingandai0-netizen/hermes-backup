# Canvas LMS File Download Reference

## Authentication Flow
1. Navigate to `https://{domain}/login/canvas`
2. Enter email in textbox "Email"
3. Enter password in textbox "Password"
4. Click button "Log In"
5. After login, URL redirects to `/courses/xxx/modules` or dashboard

## File Download Workflow
1. Navigate to file page: `https://{domain}/courses/{course_id}/files/{file_id}`
2. Page shows:
   - File heading: `FE7066SR Assessment 2 Submission Form 70%.docx`
   - Download link: `Download FE7066SR Assessment 2 Submission Form 70%.docx` (ref=e21)
   - File size: `(698 KB)`
   - Iframe preview: often "403 Forbidden" (ignore)
3. Click the download link to trigger browser download
4. Check `~/Downloads/` for the file

## Canvas REST API (for metadata)
```
GET /api/v1/courses/{course_id}/files/{file_id}
```
Response includes:
- `id`: 208781
- `folder_id`: 29310
- `display_name`: "FE7066SR Assessment 2 Submission Form 70%.docx"
- `filename`: "FE7066SR+Assessment+2+Submission+Form+70%25.docx"
- `upload_status`: "success"
- `content-type`: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
- `url`: "https://stanfort.instructure.com/files/208781/download?download_frd=1"
- `size`: 714985
- `created_at`: "2026-03-13T03:28:06Z"
- `updated_at`: "2026-05-21T06:54:49Z"
- `canvadoc_session_url`: "/api/v1/canvadoc_session?blob=..." (for iframe preview)

## Course Structure (MSc-IAF - November 2025)
- Course ID: 966
- Modules visible: ORIENTATION KIT, BENCHMARK & TARGETS, AC7071SR, AC7073SR, FE7P64SR, FE7066SR
- FE7066SR = Data Analysis for Global Business
- Files under FE7066SR module:
  - Module Handbook
  - Assessment 1 Submission Form (30%)
  - Assessment 2 Submission Form (70%)
  - Weekly lesson slides (Week 1-12)

## curl Download Pitfall
```bash
# This returns the LOGIN PAGE (23KB HTML), not the file:
curl -L -o file.docx "https://stanfort.instructure.com/files/208781/download"
# Because session cookie is HttpOnly, not accessible via document.cookie
# Use browser_click instead of curl for authenticated downloads
```
