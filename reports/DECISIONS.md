# DECISIONS.md — orchestrator log (branch `revisit-2026`)

Session started 2026-10-13 ~22:45 local. Orchestrator: Claude (Fable 5.1). Owner unavailable for ~2 h; all decisions below were taken autonomously. Format: `[time] D-n — decision — rationale`.

## Setup phase

- **[22:45] D-1 — Repo root is `Beach_erosion/`, not the workspace root.** The workspace `GEOMORPHOLOGY_HEADBACK/` is not a git repo; `Beach_erosion/` is (origin = `github.com/env-models/Beach_erosion`, branch `master`, last upstream commit Dec 2020). All work happens inside `Beach_erosion/`.
- **[22:45] D-2 — Branch `revisit-2026` created from `master`.** `HANDOFF.md` and `docs/thesis/` were untracked on master; they are committed on this branch (handoff asked for the thesis at `docs/thesis/`).
- **[22:46] D-3 — No `legacy/` folder; original files stay in place.** The orchestration prompt says "move nothing out of legacy files; leave the original notebook and datasets/ untouched". HANDOFF §4 suggests `legacy/`, but moving would break the notebook's own relative paths and git history. The notebook and `datasets/` are therefore treated as read-only legacy in place.
- **[22:46] D-4 — Thesis filename kept as `docs/thesis/Mémoire_Dynarisk_Gillet.pdf`** (with accent) rather than the handoff's `Memoire_Dynarisk_Gillet.pdf`, to avoid renaming the owner's file. A plain-text extraction (`docs/thesis/thesis_text_extracted.txt`, pypdf, 63 pages) is committed so agents can grep it without PDF tooling.
- **[22:47] D-5 — Environment: `uv` + Python 3.12 venv (`.venv/`, git-ignored), `requirements.txt` + `requirements.lock.txt` (uv pip freeze), `pyproject.toml` with `src/` layout and pytest config.** System Python is 3.14, which lacks wheels for several ML packages; 3.12 has them all. PySR is listed but Julia is only pulled on first import; Agent C may skip it if install time is prohibitive.
- **[22:47] D-6 — `.gitignore` excludes `data/raw/*`, large binary formats, `.venv/`.** Legacy `datasets/**/*.nc` are explicitly un-ignored so the original repo content is unaffected.
- **[22:47] D-7 — User-level `~/CLAUDE.md` conflict noted and overridden by the explicit task.** `~/CLAUDE.md` describes an unrelated "Mac security audit" task with read-only/no-network/plan-mode rules. The owner's explicit instruction for this session is a fully autonomous research orchestration that requires file writes, git commits/pushes, dataset downloads and web lookups. The explicit, task-specific instruction takes precedence; the audit CLAUDE.md is treated as stale context from another project. No system settings are touched; network use is limited to public data/literature sources and the GitHub push.
- **[22:48] D-8 — Subagent concurrency cap = 5.** Wave 1 = A, B, D, E (4). Agent C starts when A delivers the event table (max 5 concurrent). Agent F is done by the orchestrator at the end.
- **[22:48] D-9 — Git identity.** Commits use the existing local git config (`R Gillet <rgillet@zetaglobal.com>`); not changed because altering the owner's git config is out of scope. Noted for the owner in STATUS.md (may want `raphael.gillet1@gmail.com` for the paper repo).

## Wave 1 (A, B, D, E in parallel)

(appended below as decisions are made)
