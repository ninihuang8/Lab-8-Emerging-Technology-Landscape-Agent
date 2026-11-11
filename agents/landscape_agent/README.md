# Emerging Technology Landscape Agent
v0.2-student | Evidence assessed 2026-11-10 America/New_York

This prompt-based specialist evaluates decision-relevant alternatives, complements, evidence gaps and reassessment signals. It uses the instructor's frozen ChatGPT/Codex workflow; it is not a live scheduling system and does not call an API.

From repository root:

```bash
python tools/check_frozen_core.py
python tools/build_prompt.py --agent agents/landscape_agent --case agents/landscape_agent/cases/primary.json
```

Open the generated work/landscape_agent_primary_prompt.txt in ChatGPT and request one JSON-only response. Save the unedited response to agents/landscape_agent/responses/ and run:

```bash
python tools/validate_response.py agents/landscape_agent/responses/primary_response.json
python agents/landscape_agent/tests/verify.py
```

The extra independent check needs the `jsonschema` Python package; the course tools require only the standard library. The source register is embedded in specialist_instructions.md because the unmodified prompt builder does not load external evidence files. For later decisions refresh original sources and synchronize the embedded register before rebuilding packets.

Primary: wafer-fab scheduling, hypothetical fast follower, human-approved six-month advisory boundary. Contrast 1: drafts-only IT service desk. Contrast 2: legacy fab with incomplete data and adversarial sales assertions. Original v0.1 response and instructions are preserved. tests/extra_field_probe.json is a constructed validator diagnostic, not a model output.

See records/quality_review.md for substantive findings and independent-review limits, evidence/source_register.md for source scope, and records/landscape_handoff.md for comparison and monitoring. Section F in the official Agent Record requires Nini's own review. This package does not authorize production actions.
