# Word Form Filling Workflow

When asked to fill in an existing .docx form/template (e.g., university forms, application forms, government forms) with user-provided data.

## Step 1: Inspect form structure

```bash
officecli view <form.docx> text                    # overview of all tables
officecli get <form.docx> '/body/tbl[1]' --depth 3 # detailed table structure with paraIds
```

Key info to extract:
- **paraId** of each fillable paragraph (stable IDs, won't shift on edit)
- Which cells are headers vs. fillable fields
- Table numbering (tbl[1], tbl[2], etc.)

## Step 2: Identify field mapping

Map user data to form fields:
- Personal details (name, ID, date of birth) → usually in first table
- Data rows (modules, items, dates) → middle tables
- Description/narrative text → large cell with empty paragraphs
- Checkboxes/ticks → specific paragraphs with option text
- Signature/date → last table

## Step 3: Batch fill with stable IDs

Use `officecli batch` with paraId-based addressing:

```bash
cat << 'EOF' | officecli batch <form.docx> --force --json
[
  {"op":"set","path":"/body/tbl[1]/tr[3]/tc[1]/p[@paraId=ABC123]","props":{"text":"Surname : SMITH"}},
  {"op":"set","path":"/body/tbl[1]/tr[3]/tc[1]/p[@paraId=DEF456]","props":{"text":"Full Time"}},
  {"op":"set","path":"/body/tbl[2]/tr[1]/tc[1]/p[@paraId=GHI789]","props":{"text":"Description text here"}}
]
EOF
```

### Addressing patterns
- Table cell: `/body/tbl[N]/tr[M]/tc[K]/p[@paraId=XXXX]`
- Paragraph: `/body/p[@paraId=XXXX]`
- Always use paraId for stability — positional indices shift on insert

### Valid paragraph props
`text`, `style`, `alignment`, `bold`, `italic`, `font` (not `font.size` — use `size`), `color`, `spaceBefore`, `spaceAfter`, `lineSpacing`, `indent`

### Checkbox handling
Use Unicode checkbox characters in text:
- ☑ for checked: `"props":{"text":"☑ Option text"}`
- ☐ for unchecked: `"props":{"text":"☐ Option text"}`

## Step 4: Fill empty rows for data tables

When form has empty rows for data entry (e.g., module codes, line items):
1. Inspect the empty row structure: `officecli get <file> '/body/tbl[1]/tr[6]' --depth 2`
2. Note the paraIds for each cell in the row
3. Fill each cell separately in the batch

## Step 5: Fill description/narrative sections

Large empty cells (like "Describe your circumstances") have multiple empty paragraphs:
1. Fill the first paragraph with the opening statement
2. Fill subsequent paragraphs with supporting details
3. Leave remaining paragraphs empty (don't fill all of them)

## Step 6: Handle declaration/signature sections

- Checkbox confirmation: replace text with ☑ + original text
- Signature line: replace placeholder with name
- Date field: fill with current date (DD/MM/YYYY format)

## Step 7: Verify

```bash
officecli query <form.docx> 'paragraph:contains("KEYWORD")'  # verify specific fields
officecli view <form.docx> text                                # full text overview
```

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|-----------------|
| `--prop font.size=10pt` | Use `--prop size=10pt` — `font.size` is NOT a valid paragraph prop |
| Using positional indices | Always use `@paraId=` — positions shift when content changes |
| Filling all empty paragraphs | Only fill as many as needed, leave the rest empty |
| Forgetting `--force` | Use `--force` on batch to bypass protection checks |
| Not verifying after fill | Always run `officecli query` to confirm key fields were written |
| Checkbox as image | Use Unicode ☑/☐ characters in text, not images |

## Example: University Mitigating Circumstances Form

```bash
# 1. Inspect
officecli get form.docx '/body/tbl[1]' --depth 3

# 2. Batch fill personal details + module rows + description + signature
cat << 'EOF' | officecli batch form.docx --force --json
[
  {"op":"set","path":"/body/tbl[1]/tr[3]/tc[1]/p[@paraId=55DBCFA8]","props":{"text":"Surname : DAI    First names: XINGAN    Student ID: 25028666"}},
  {"op":"set","path":"/body/tbl[1]/tr[6]/tc[1]/p[@paraId=330CD0D4]","props":{"text":"AC7071SR"}},
  {"op":"set","path":"/body/tbl[1]/tr[6]/tc[2]/p[@paraId=61D87DC3]","props":{"text":"International Financial Reporting"}},
  {"op":"set","path":"/body/tbl[2]/tr[2]/tc[1]/p[@paraId=5BCB08D9]","props":{"text":"I am writing to request an intermission..."}},
  {"op":"set","path":"/body/tbl[3]/tr[3]/tc[1]/p[@paraId=2773333D]","props":{"text":"☑ No ..."}},
  {"op":"set","path":"/body/tbl[4]/tr[2]/tc[1]/p[@paraId=606E51F2]","props":{"text":"☑ I confirm that I have read..."}},
  {"op":"set","path":"/body/tbl[4]/tr[2]/tc[1]/p[@paraId=488EAB2D]","props":{"text":"Student's Signature: DAI XINGAN    Date: 05/08/2026"}}
]
EOF

# 3. Verify
officecli query form.docx 'paragraph:contains("DAI")'
```
