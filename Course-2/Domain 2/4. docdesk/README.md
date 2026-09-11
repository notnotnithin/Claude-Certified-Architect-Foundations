# Demo 4 — MCP Server Integration (DocDesk)

Fourth demo in **Domain 2: Tool Design & MCP Integration**, continuing DocDesk.
Maps to **Task Statement 2.4 — Integrate MCP servers into Claude Code and agent
workflows.**

> **Read this first — this demo is mostly configuration.**
> Demos 1–3 were runnable Python you watch produce output. Task 2.4 is largely
> about **configuration** — wiring MCP servers into Claude Code with `.mcp.json`
> and `~/.claude.json`. So this demo is a **config walkthrough** with two
> **runnable** pieces on top: a script that shows secret/`${VAR}` expansion, and
> a client that connects to the real MCP server so you can *see* its tools and
> resources live. Explain the configs, then run those two to prove them.

---

## The concepts (short & simple)

**1. What is an MCP server?**
A small program that gives Claude Code extra **tools** (actions) and **resources**
(readable content). You don't build these tools into your app — Claude Code
connects to the server and uses them.

**2. Two places to configure servers — scope matters:**

| Config file | Scope | Who gets it | Use for |
|-------------|-------|-------------|---------|
| `.mcp.json` (repo root) | **project** | everyone who clones the repo | shared team tooling |
| `~/.claude.json` (home dir) | **user** | only you | personal / experimental servers |

Put a server the **whole team** needs in `.mcp.json` (it's committed to git).
Put a **personal** server only you use in `~/.claude.json` (never shared).

**3. Never commit secrets — use env-var expansion.**
In `.mcp.json` you write `${GITHUB_TOKEN}`, not the real token. Claude Code
expands it from your environment at connection time. This lets you safely commit
`.mcp.json` while keeping secrets out of the repo.

**4. All configured servers are available at once.**
When Claude Code starts, it connects to every configured server and discovers
their tools **at connection time**. The agent then sees all of them together.

**5. MCP resources = a content catalog.**
A **tool** is an action ("search the docs"). A **resource** is readable content
("here is the list of docs"). Exposing a catalog as a resource lets the agent
**see what exists without spending tool calls** to discover it.

**6. Community server vs custom server.**
For a **standard** integration (GitHub, Jira, Slack), use an existing
**community** MCP server — don't reinvent it. Write a **custom** server only for
**team-specific** needs (like our DocDesk document store).

**7. Good MCP tool descriptions win adoption.**
Claude Code also has built-in tools. If your MCP tool's description is vague, the
agent may prefer a built-in instead. Write detailed descriptions so the agent
picks your more-capable MCP tool.

---

## The files in this demo

| File | What it shows |
|------|---------------|
| `.mcp.json` | **Project-scoped** config (committed). A custom `docdesk` server + a community `github` server, both using `${ENV_VAR}` for secrets. |
| `claude_user_config_example.json` | An example of a **user-scoped** `~/.claude.json` for a personal/experimental server. Rename/copy to `~/.claude.json`. |
| `mcp_servers/docdesk_server.py` | A real custom MCP server: two **tools** (search/load) + one **resource** (the document catalog). This is what `.mcp.json` points to. |
| `expand_config.py` | **Runnable** — shows `${ENV_VAR}` expansion in `.mcp.json` (secrets injected at load time). |
| `test_client.py` | **Runnable** — connects to the MCP server (same protocol Claude Code uses) and shows its tools + resource live. |
| `documents/` | The documents the DocDesk server serves. |
| `.env.example` | The env vars that `.mcp.json` expands (`DOCDESK_DOCS_DIR`, `GITHUB_TOKEN`). |
| `.gitignore` | Keeps `.env` and `~/.claude.json` out of the repo. |

`requirements.txt` (outside) lists `mcp`, needed only if you want to launch the
custom server yourself.

---

## Walkthrough — read the configs in this order

**1. Open `.mcp.json`.** Notice:
- Two servers under `mcpServers`: our custom `docdesk` and the community
  `github`.
- Secrets use `${GITHUB_TOKEN}` / `${DOCDESK_DOCS_DIR}` — no real values. That's
  why this file is safe to commit (Concept 3).
- Because it's in the repo root, every teammate who clones gets both servers
  automatically (Concept 2, project scope).

**2. Open `claude_user_config_example.json`.** This is what a **personal**
server looks like. It lives at `~/.claude.json` (your home directory), is NOT in
the repo, and only you get it (Concept 2, user scope). Both the project and user
servers are available to Claude Code **at the same time** (Concept 4).

**3. Open `mcp_servers/docdesk_server.py`.** This is the custom server
`.mcp.json` points to. See the two **tools** (with detailed descriptions so the
agent prefers them over built-ins — Concept 7) and the one **resource**
(`docdesk://catalog`) that lists the documents so the agent doesn't have to
search just to find out what exists (Concept 5).

**4. Open `.env.example`.** These are the variables `.mcp.json` expands. Copy to
`.env` and fill in real values (Concept 3).

---

## How it fits together

```
Claude Code starts
      │
      ▼
reads .mcp.json (project)   +   ~/.claude.json (user)      ← Concept 2 (both scopes)
      │
      ▼
expands ${GITHUB_TOKEN}, ${DOCDESK_DOCS_DIR} from env       ← Concept 3 (no secrets in file)
      │
      ▼
connects to every server, discovers tools + resources      ← Concept 4 (all at once)
      │
      ├─ docdesk (custom)  → tools: search_documents, load_document
      │                      resource: docdesk://catalog     ← Concept 5 (catalog)
      │
      └─ github  (community) → GitHub tools                  ← Concept 6 (community over custom)
      │
      ▼
agent now uses all these tools; good descriptions make it   ← Concept 7 (adoption)
prefer the MCP tools over generic built-ins
```

---

## Run it — two things you CAN show live

Most of Task 2.4 is configuration, but two parts are genuinely runnable, so you
can **explain the configs, then run these to prove them.**

First install the dependencies (from the folder with `requirements.txt`):
```bash
pip install -r requirements.txt
```
Then create your `.env` from the template (this holds the values `.mcp.json`
expands):
```bash
# Windows:  copy .env.example .env
# mac/Linux: cp .env.example .env
```

### Part B — env-var expansion (`expand_config.py`)
Shows how `${VAR}` in `.mcp.json` gets filled in from your environment at load
time — so the secret is never in the config file.

This script reads your **`.env`** file automatically (via `load_dotenv()`), so
you just edit `.env` and run — no `set`/`export` commands needed.

```bash
# 1) With the values COMMENTED OUT in .env, run — placeholders stay unresolved:
python expand_config.py
```
`.env` (before):
```dotenv
# DOCDESK_DOCS_DIR=./documents
# GITHUB_TOKEN=ghp_demo123
```

```bash
# 2) UNCOMMENT the two lines in .env, save, then run again — they fill in:
python expand_config.py
```
`.env` (after):
```dotenv
DOCDESK_DOCS_DIR=./documents
GITHUB_TOKEN=ghp_demo123
```

You'll see `${GITHUB_TOKEN}` become the real value only once it's in `.env` —
proving the secret lives in `.env` (which is git-ignored), not in the committed
`.mcp.json`. Notice the **BEFORE** section is identical in both runs: the
`.mcp.json` file itself never changes; only the expanded **AFTER** result does.

### Part A — connect to the MCP server (`test_client.py`)
Connects to `docdesk_server.py` over MCP (the **same protocol Claude Code uses**)
and shows exactly what Claude Code sees on connect: the server's **tools**, its
**resource** (the catalog), a real tool **call**, and a resource **read**.

```bash
python test_client.py
```
Expected output (abridged):
```
TOOLS discovered on the server:
  • search_documents   Find WHICH DocDesk documents mention a keyword...
  • load_document      Load the FULL text of ONE DocDesk document...

RESOURCES discovered on the server:
  • docdesk://catalog  —  document_catalog

CALLING tool: load_document('returns_policy.md')
  { "name": "returns_policy.md", "text": "# PyStack Mart — Returns Policy ..." }

READING resource: docdesk://catalog
  Available DocDesk documents:
  - product_faq.md
  - returns_policy.md
```
This proves the server you configured in `.mcp.json` is real, and makes
**tools vs resources** concrete: a tool is an action you *call*; a resource is
content you *read*.

> **What still can't run:** the Claude-Code-specific wiring — `.mcp.json` vs
> `~/.claude.json` scoping and "all servers discovered at connect time" — only
> happens inside a real Claude Code session. Explain those from the config files;
> the two scripts above cover everything that has a runnable form.


## Key decisions to remember (exam-focused)

- **Team tool → `.mcp.json` (project).  Personal tool → `~/.claude.json` (user).**
- **Secrets → `${ENV_VAR}` expansion**, never hard-coded in the config.
- **Standard integration → community server. Team-specific → custom server.**
- **A catalog/index → expose it as a resource**, so the agent doesn't waste tool
  calls discovering what exists.
- **Write detailed MCP tool descriptions** so the agent prefers them over
  built-in tools.
