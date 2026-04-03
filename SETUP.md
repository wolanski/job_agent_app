# Antigravity setup (recommended for Process Steward workflow)

This guide aligns Antigravity configuration with the **doc-driven Process Steward** approach.

## 1) Choose the right conversation mode

Antigravity supports **Planning** vs **Fast** conversation modes:
- Use **Planning** for: architecture, contracts, decomposition, multi-file refactors, anything “non-trivial”.
- Use **Fast** for: small edits, quick fixes, mechanical refactors.

(See the Antigravity codelab explanation of Planning vs Fast.) 

## 2) Configure security and autonomy policies

Antigravity exposes policies for **terminal execution**, **artifact review**, and **browser JavaScript execution** in setup and settings. The codelab explains these policies and the tradeoffs. 

**Recommended baseline** (safe + effective):
- Terminal auto-exec: **Auto** or **Request review** (start conservative; relax later)
- Review policy: **Agent Decides** or **Request Review**
- Browser JS execution: **Request review** (tighten if you handle untrusted pages)

## 3) Configure Terminal Allow/Deny lists

Antigravity supports a command allow list and deny list. The codelab demonstrates using **Deny List** entries like:
- `rm`, `rmdir`, `sudo`, `curl`, `wget`

Recommendation:
- Start with a conservative policy + deny list.
- Promote safe project commands later (start by allowlisting `make check`) (e.g., `make check`, `uv sync`, `uv run pytest`) once you trust your repo.

> You may need to restart Antigravity for allow/deny list changes to take effect (per codelab).

## 4) Configure Browser Allowlist

Antigravity stores a browser allowlist file under:
- `HOME/.gemini/antigravity/browserAllowlist.txt`

Recommendation:
- Put only trusted domains there for agent browsing (docs, your app domains, localhost, etc).
- Keep it minimal; expand intentionally.

## 5) Configure Rules & Workflows locations (global vs workspace)

Per the codelab, Antigravity supports:
- Global rule: `~/.gemini/GEMINI.md`
- Global workflows: `~/.gemini/antigravity/global_workflows/*.md`
- Workspace rules: `<repo>/.agents/rules/`
- Workspace workflows: `<repo>/.agents/workflows/`

Recommendation:
- Keep this process **workspace-scoped** (inside the repo) so it’s versioned with code.
- Optionally add a global rule that says: “always follow workspace process rules if present”.

## 6) Optional: Skills (lazy-loaded instructions)

Antigravity supports workspace **skills** that carry metadata (name/description) and load full instructions only when needed.
This pack includes an optional skill:
- `.agents/skills/process-steward/SKILL.md`

Recommendation:
- Keep the always-on **rules** short.
- Put longer “how-to” guidance in the skill so the agent loads it only when relevant.

---
If you need to tighten agent compliance further, see:
- `.agents/rules/process-steward.md`
- `process/PROCESS_REFERENCE.md`


## 7) Deterministic validation entrypoint
This repo defines a single validation entrypoint:
- `make check`

Recommendation:
- Configure Terminal policy to allow `make check`.
- Treat `make check` as the Definition-of-Done gate.
