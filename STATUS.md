# STATUS.md — revisit-2026 (live; rewritten at end of session)

**Session:** 2026-10-13 evening, autonomous orchestration, ~2 h budget. See `reports/DECISIONS.md` for every decision.

## Resume instructions (if this session dies)
1. `git checkout revisit-2026 && source .venv/bin/activate` (recreate with `uv venv --python 3.12 .venv && uv pip install -r requirements.lock.txt && uv pip install -e .`).
2. Read `reports/DECISIONS.md`, then the per-agent reports under `reports/`.
3. Wave plan: A (audit, `src/evi/`, event table) ∥ B (data) ∥ D (state of the art) ∥ E (supervisors) → C (modelling, after A's event table) → F (paper outline + checklist, orchestrator) → this file.

## Progress
- [x] Setup: branch, layout, env, thesis text extraction, first commit + push (22:50)
- [ ] Wave 1 launched (A, B, D, E)
- [ ] Event table v1 from A
- [ ] Wave 2: C
- [ ] paper/outline.md + publication checklist
- [ ] Final STATUS.md, commit, push
