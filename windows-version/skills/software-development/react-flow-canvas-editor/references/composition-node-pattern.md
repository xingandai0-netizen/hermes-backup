# Export → Composition Node Evolution

## Problem
Simple export/download nodes are insufficient for AI workflow platforms. Users need to specify HOW to process upstream media, not just download it.

## Evolution Pattern

### Before (Simple Export)
- Input: IMAGE or VIDEO from upstream
- UI: Preview + Download button
- No model selection, no prompt, no API call
- Just displays what comes in

### After (Composition Node)
- Input: IMAGE or VIDEO from upstream
- UI: Model selector + Prompt textarea + Compose button + Progress + Preview + Download
- Calls AI API with upstream media URL + user prompt + selected model
- Produces NEW media based on user instructions
- Output: Transformed IMAGE or VIDEO (can chain to next node)

## Key Requirements (User Feedback)
1. "那为什么没有选择模型的地方？" → MUST have model dropdown
2. "不选择模型你知道用户要合成什么视频吗" → Model determines output
3. "你怎么把要求传递给模型合成" → Need prompt textarea
4. "你来合成吗？？？" → The node calls the API, not the agent

## Implementation Checklist
- [ ] Model selection dropdown (hardcoded verified models)
- [ ] Prompt/instruction textarea
- [ ] Input validation (upstream connected? prompt filled? API configured?)
- [ ] API call with: upstream URL in prompt + user prompt + selected model
- [ ] Async polling for result
- [ ] Progress indicator
- [ ] Output preview (image/video)
- [ ] Download link
- [ ] Both input AND output handles (for chaining)

## Node Types That Need This Pattern
- ImageExportNode → "图片合成" (compose images)
- VideoExportNode → "视频合成" (compose videos)
- Any future "processing" node that calls AI APIs

## Node Types That Do NOT Need This
- ImageProcessNode (local operations like crop/resize)
- SizeAdapterNode (local dimension changes)
- Import nodes (file upload only)
