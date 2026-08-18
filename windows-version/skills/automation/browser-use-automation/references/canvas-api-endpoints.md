# Canvas LMS File Download - API & Debug Reference

## File API Endpoint
```
GET https://stanfort.instructure.com/api/v1/courses/{course_id}/files/{file_id}
```
Returns JSON with:
- `id`, `folder_id`, `display_name`, `filename`
- `content-type`: e.g. `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- `url`: download URL (`https://stanfort.instructure.com/files/{file_id}/download?download_frd=1`)
- `size`: file size in bytes (714,985 for this docx)
- `created_at`, `updated_at`, `modified_at`
- `locked`, `hidden`, `locked_for_user`, `hidden_for_user`
- `canvadoc_session_url`: iframe preview URL

## Download URL Pattern
```
https://stanfort.instructure.com/files/{file_id}/download?download_frd=1
```

## Observed Failure Modes
1. **curl without auth cookie** → Returns login HTML page (~23KB), HTTP 200 (deceptive — no redirect)
2. **curl with only `_csrf_token`** → Same: returns login page
3. **Browser fetch() with credentials** → `Failed to fetch` (CSP/CORS policy)
4. **Browser iframe preview** → `403 Forbidden` (normal for Canvadocs)
5. **Direct browser click on download link** → Works (full session in browser)

## Key Insight
Canvas returns HTTP 200 even for unauthenticated download requests — the body is the login page HTML, not a redirect. This makes it look like the download succeeded in curl (`100 23722` = 23KB of login HTML). Always verify downloaded file type with `file` command.

## Session Info
- Course: MSc-IAF - November 2025 (ID: 966)
- File: FE7066SR Assessment 2 Submission Form 70%.docx (ID: 208781)
- Expected size: 714,985 bytes
- Login URL: https://stanfort.instructure.com/login/canvas
