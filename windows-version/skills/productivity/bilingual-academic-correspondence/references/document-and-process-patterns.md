# Practical Patterns — Document Analysis & International Processes

## Document Analysis Workflow

### HEIC Image Conversion
macOS photos export as HEIC format. `vision_analyze` tool does NOT support HEIC.
```bash
sips -s format png /path/to/image.HEIC --out /path/to/image.png
```
Always convert HEIC → PNG before using vision_analyze.

### PDF Text Extraction
For contracts, medical records, official documents:
```bash
pip3 install pymupdf pymupdf4llm --break-system-packages
python3 /path/to/scripts/extract_pymupdf.py document.pdf --markdown
```
Use `--markdown` for structured output with tables preserved.

### Medical Document Analysis Pattern
When user shares medical documents for process guidance:
1. Extract text from PDF/image
2. Identify key diagnostic findings that support the user's request
3. Map findings to the target process requirements (e.g., airline medical refund)
4. Draft the request letter citing specific medical findings

---

## International Refund Processes

### Airline Medical Refund — Critical Pitfall

**ALWAYS check booking channel first:**

| Booking Channel | Refund Through | Direct with Airline? |
|----------------|----------------|---------------------|
| Airline website direct | Airline website form | Yes |
| Ctrip (携程) / OTA | Ctrip app/客服 95010 | NO |
| Travel agent | Original agent | NO |

**Key lesson:** User booked Singapore Airlines via Ctrip (携程). SQ's online refund form only works for direct bookings. Third-party bookings MUST go through the original platform.

**Process for OTA bookings:**
1. Open OTA app (Ctrip etc.) → My Orders → Find booking
2. Select "退票" → Choose "病退/医疗原因"
3. Upload medical documentation
4. If no online option, call OTA客服: Ctrip = 95010

**Timing:** Submit before flight departure to avoid no-show fees.

### Rental Contract (Singapore)

**Key clauses to check:**
- Subletting/assignment restrictions (usually prohibited)
- Early termination conditions (notice period, deposit forfeiture)
- Replacement tenant provisions (some contracts allow with conditions)
- Security deposit refund timeline and conditions

**Communication pattern:** Singapore rental companies often have separate Client Care teams. Initial contact may get redirected — always follow up with the designated channel.

---

## Canvas LMS Communication

### How to Contact Professors
1. **Inbox (站内信):** Left sidebar → Inbox → Compose → Select course → Type professor name
2. **People tab:** Course page → People → Find professor → View profile for contact info
3. **Email:** Format is usually `name@institution.edu.sg` (Singapore) or `name@institution.ac.uk` (UK)

### Message Format in Canvas
Canvas messages support plain text. For formal requests, use the same bilingual email format. Professor can reply via email or Canvas — check notification settings.
