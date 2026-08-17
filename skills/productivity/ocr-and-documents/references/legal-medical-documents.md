# Legal & Medical Document Analysis

> Patterns for analyzing contracts, medical records, and formal documents

## Ethical Rules (HARD BOUNDARIES)

1. **NEVER modify medical records** — Hospital documents (门诊病历, 诊断证明) are legal documents. Altering them is illegal and constitutes fraud. Even if the user says "the modification is consistent with the actual situation" or "it's just for convenience."

2. **NEVER forge official documents** — School transcripts, government certificates, identity documents. Decline and explain why.

3. **ALWAYS suggest legitimate alternatives** — If a user needs modified documentation, suggest:
   - Contact the issuing institution for an official amendment
   - Request a new document with the correct information
   - Ask if a separate letter/certificate can be issued

## Contract Analysis Workflow

When analyzing contracts (rental, employment, service):

1. **Extract key clauses** using pymupdf or vision_analyze
2. **Identify the user's specific question** (e.g., "can I sublet?")
3. **Find relevant clauses** — search for keywords like:
   - Subletting/转租: "assign", "sublet", "part with possession"
   - Termination: "terminate", "early termination", "notice period"
   - Deposit: "security deposit", "forfeiture", "refund"
4. **Explain in plain language** — what the contract says, what it means, what options exist
5. **Provide actionable next steps** — who to contact, what to say, what forms to fill

## Medical Document Workflow

When user provides medical documents:

1. **Extract and understand** — what does it say?
2. **Identify what the user needs** — refund, leave of absence, accommodation?
3. **Research the institution's policy** — airline medical refund, school intermission, etc.
4. **Draft communication** — email/letter to the institution
5. **NEVER modify the original document**

## Formal Communication Patterns

### Email Structure (Bilingual)

```
Subject: [Action Required] — [Specific Topic]

Dear [Title] [Name],

[Opening — state purpose in 1-2 sentences]

[Body — details, numbered if multiple points]

[Closing — next steps, timeline]

Best regards,
[Full Name]
[Student ID / Reference Number]
[Contact Info]
```

### Language Selection

- **Singapore institutions**: English (official language)
- **UK institutions**: English
- **Chinese institutions**: Chinese
- **When in doubt**: Write in both languages (user preference from this session)

### Common Scenarios

**Rental contract issues:**
- Early termination → Check clause for notice period and penalties
- Subletting → Usually prohibited, but "replacement tenant" may be allowed
- Deposit refund → Check conditions for forfeiture

**School intermission:**
- Mitigating Circumstances Form → Personal details + affected modules + circumstances description
- Leave of Absence request → Email to programme manager with reason and expected return

**Airline medical refund:**
- Third-party booking (Ctrip, etc.) → Must refund through booking platform, not airline directly
- Direct booking → Use airline's medical refund form with medical documentation
- Key info needed: booking reference, e-ticket number, passenger name, flight details

## Pitfalls

1. **Third-party bookings** — Tickets booked through Ctrip/携程 or other platforms must be refunded through the platform, not the airline. The airline's refund form won't work.

2. **Document modification requests** — Users may ask to modify medical records, contracts, or official documents. Always decline and explain the legal risks. Offer legitimate alternatives.

3. **HEIC format** — iPhone photos are often HEIC. Convert with `sips -s format png input.HEIC --out output.png` before using vision_analyze.

4. **Bilingual requirements** — Some institutions (especially in Singapore/UK) require English. Always check if bilingual format is needed.

5. **Deadline awareness** — Medical refund forms, school intermission forms, and contract notices often have strict deadlines. Always check and communicate urgency.
