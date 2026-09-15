# 👻 Fiverr Phantom

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![MCP: Enabled](https://img.shields.io/badge/Model_Context_Protocol-Enabled-purple.svg)](https://modelcontextprotocol.io/)
[![Engine: Patchright Stealth](https://img.shields.io/badge/Engine-Patchright%20Stealth-orange.svg)]()

> **Fiverr Phantom** is an autonomous, anti-ban automation suite and Model Context Protocol (MCP) server for Fiverr sellers. Built on C++ stealth-patched Chromium (`Patchright`), it eliminates bot detection flags and enforces humanized behavioral heuristics (micro-jitter, variable keystrokes, non-linear scrolling) to safely manage profiles, update bios, bulk-add search-indexed skills, and interface directly with AI coding assistants (Claude Desktop, Cursor, Antigravity).

---

## 🛡️ Anti-Ban Architecture & Evasions

Fiverr utilizes Cloudflare and PerimeterX bot mitigation. Fiverr Phantom evades detection via 4 core mechanisms:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. C++ Patched Chromium (Patchright)                        │
│    • Strips navigator.webdriver                             │
│    • Removes CDP runtime detection flags                    │
│    • Masks Canvas, WebGL, AudioContext & screen fingerprints│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Humanized Keystroke Dispatch (Gaussian Delay)            │
│    • Randomized 35ms–100ms per character                    │
│    • Natural punctuation pauses (0.2s–0.4s on . , ! \n)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. Non-Linear Mouse & Scroll Jitter                         │
│    • Staggered multi-step scrolling for lazy loaders        │
│    • Pre-click human hovering delay                         │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 4. Isolated Local Session Encryption                        │
│    • Cookies stored locally in ~/.fiverr-phantom/profile     │
│    • Zero plain-text credentials stored or transmitted     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quickstart

### 1. Installation

```bash
git clone https://github.com/modelnorth/fiverr-phantom.git
cd fiverr-phantom
pip install -e .
```

Or run instantly via `uv`:

```bash
uv run --with patchright fiverr-phantom --help
```

---

### 2. Connect Your Account (One-Time Interactive Login)

Launch a visible stealth browser window to log in:

```bash
fiverr-phantom --login
```
* Complete your email/password login and 2FA challenge.
* Once the seller dashboard appears, close the browser window.
* All authentication cookies are safely stored in your local persistent profile (`~/.fiverr-phantom/profile`).

---

### 3. Verify Session Health

```bash
fiverr-phantom --status
```

---

### 4. Optimize Profile Bio & Tagline

```bash
fiverr-phantom --update-bio \
  --tagline "Sovereign AI Systems Architect | Defense-Grade Agent Security" \
  --description "I engineer sovereign AI infrastructure, autonomous multi-agent orchestration, and defense-grade security kernels for enterprise and public-sector clients."
```

---

### 5. Bulk-Add Search-Indexed Skills

```bash
fiverr-phantom --add-skills "Python,Artificial Intelligence,Machine Learning,Large Language Models (LLM),Autonomous Agents,Computer Vision,Cybersecurity,Cloud Computing" --level "Expert"
```

---

## 🔌 Model Context Protocol (MCP) Integration

Fiverr Phantom exposes native tools for AI assistants like Claude Desktop, Cursor, and Antigravity.

### Client Configuration (`mcp_config.json` or `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "fiverr-phantom": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/modelnorth/fiverr-phantom.git",
        "fiverr-phantom-mcp"
      ]
    }
  }
}
```

### Exposed MCP Tools:
* `fiverr_get_status`: Validates whether the local seller session is active.
* `fiverr_update_profile`: Updates profile description and tagline with humanized typing.
* `fiverr_add_skills`: Bulk-adds search-indexed skills with experience level.

---

## 📜 License & Disclaimers

Licensed under the [MIT License](LICENSE).

*Disclaimer: This is an independent, community-driven open-source project and is not affiliated with, endorsed by, or sponsored by Fiverr International Ltd. Users are responsible for adhering to Fiverr's Terms of Service.*
