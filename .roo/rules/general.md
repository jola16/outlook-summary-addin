# General agent rules (all projects)

These rules apply to all repositories and all coding agents (Roo Code, GitHub Copilot, etc.).
Project-specific rules are in each project's `AGENTS.md`.

## General rules

- Always respond to the user in Swedish, unless the user writes in another language — then match that language.
- Use English for all comments, documentation, and commit messages.
- Keep changes as small and coherent as possible.
- Prefer refactoring over adding duplicate logic.
- Always try to understand the existing architecture and follow the established patterns before introducing new ones.
- Keep all answers short — get to the point fast. Keep summaries brief and bullet points only.
- After completing a feature or fix, always use `ask_followup_question` to confirm with the user that the code is ready for review using the **DoD Checklist**.
- Before you want to run linting (e.g., ruff, pylint) during development, always use `ask_followup_question` to confirm that the user wants to do that now.
- Before you want to run tests during development, always use `ask_followup_question` to confirm that the user wants to do that now.

## Terminal / shell

**Always use PowerShell syntax.** The terminal in VSCode on this machine runs PowerShell 7.
The system prompt may say `cmd.exe` as the default shell — ignore that; VSCode always opens
PowerShell terminals.

- Use `Remove-Item` not `rm`, `Copy-Item` not `cp`, `Move-Item` not `mv`
- Use `Get-ChildItem` not `ls`, `Write-Output` not `echo` (for variables)
- Use `;` to chain commands, not `&&`
- Do **not** use Unix utilities like `grep`, `sed`, `awk`, `cat` — use PowerShell equivalents
  (`Select-String`, `Get-Content`, etc.) or Python one-liners instead

## File editing workflow

When editing a file:

1. Try to use the `apply_diff` tool, making sure the diff uses the correct format.
2. If that fails, re-read the relevant section, recalculate the diff, and try `apply_diff` again.
3. If that still fails, re-read the whole file, recalculate the diff, and try `apply_diff` one more time.

## Definition of done (DoD) Checklist

### DoD Pre-Requisite

Only run the **Definition of Done** checklist when the user has confirmed that it should be run. This is further defined in the general rules.

### Rules for running the checklist

All checklist steps must be completed after a code change before the task can be considered as finished. Vice versa, if the checklist steps have already been completed in this session, and the code hasn't changed since then, then another run of the DoD checklist should skip the checklist steps.

### Mandatory checklist steps for DoD

1. **Lint and format** – run on **all files in the entire project** (root directory and all subdirectories)
   - `ruff check --fix .` — fix all errors in the entire project (no unsafe fixes without explicit approval).
   - `ruff format .` — format all files in the entire project.
   - `python -m pylint .` — must score 10.00/10 for all modules in the entire project.

   **Important:** Before adding disable comments, check `pyproject.toml` for any disabled rules or project-specific linting configuration (both `[tool.ruff.lint.ignore]`, `[tool.ruff.lint.per-file-ignores]`, and `[tool.pylint.'MESSAGES CONTROL'].per-file-ignores`) and respect those settings for the specific file path.

   If linting errors cannot be fixed automatically and require `# noqa` or `# pylint: disable` comments:
   - **NEVER** add these comments without explicit user approval.
   - **ALWAYS** ask the user first: "Should I add a disable comment, refactor the code, or temporarily ignore this error?"
   - Document the reason for the disable comment in the code.
   - Choose between inline disable comments (`# noqa`, `# pylint: disable`) or adding the rule to `pyproject.toml` per-file-ignores, depending on whether the exception is file-specific or project-wide.

2. **Tests** – search `tests/unit/` **and** `tests/integration/` for any test that references
   changed symbols, fields, or behaviour; update all affected tests. Every changed behaviour
   **must** have a corresponding test — do not skip this step.

3. **Run all tests** – `python -m pytest tests/` (unit **and** integration, no exceptions — never just `tests/unit/`); all must pass.

4. **Documentation and versioning** – *after* the tests are green, review and update **all** of the following:

   **4a. Update documentation:**
   - Update relevant Markdown documentation in English, including:
     - High-level docs (e.g. `docs/*.md`)
     - Architecture documentation if applicable
   - `README.md` — update if public-facing behaviour or usage changed
   - Module and function docstrings in changed source files
   - Inline comments where behaviour changed

   **4b. Decide on change type and versioning:**
   - Versioning format: `MAJOR.MINOR.PATCH` (e.g., 1.4.2)
     - **MAJOR** (first digit): Breaking changes or major feature releases
     - **MINOR** (second digit): New features or significant enhancements
     - **PATCH** (third digit): Bug fixes, minor improvements, UI tweaks
   - Decide whether the change is **minor** or **non-trivial**:
     - **Minor** = tiny fix with no behaviour change and no public surface change. Bump patch version (e.g., 1.2.1 → 1.2.2).
     - **Non-trivial** = anything else. Bump minor or major version (e.g., 1.2.0 → 1.3.0).
   - If minor or non-trivial: bump the version number in `pyproject.toml` and add an entry to `CHANGELOG.md`.
     - **Summarize changes** – identify what changed since the last commit (what, why, where) and use this as the entry in `CHANGELOG.md`.

   **4c. Update plan files (if applicable):**
   - If you have worked with a plan in the `plans/` folder, update it with a Result summary of what has been accomplished (or left out).
     - Plans in the `plans/` folder must use a `yyyy-mm-dd-` date prefix in the filename, followed by a short kebab-case description.
       Example: `plans/2026-03-04-generalize-items.md`
     - The file's top-level heading must also start with the date and a short description:
       `# yyyy-mm-dd Plan: <description>`

### After DoD completion

Once all Definition of Done steps are complete:

1. **Post a Result report** – post a dated `yyyy-mm-dd Result:` section listing:
   - All updated files (code + docs).
   - New version number (if changed).
   - Summary of what was accomplished.

2. **Ask the user** if they want to proceed with the **Commit Checklist** using `ask_followup_question`. Do NOT use `attempt_completion` after DoD is done. Instead, present the user with options to:
   - Continue with the **Commit Checklist** (run `/commit-checklist`)
   - Review specific changes before committing
   - Make additional changes

## Commit Checklist

### Commit Rules

**Always follow this checklist when changes are to be committed.**

### Commit Pre-Requisite

**A completed DoD is mandatory before any commit unless the user has agreed to skip it**

### Mandatory checklist steps for commit

1. **Select commit strategy** – Decide on commit type based on whether the change is **minor** or **non-trivial**:
   - **Minor fix** (tiny fix, no behaviour change, no public surface change):
     - Use `git commit --amend` to amend the previous commit.
     - Update the commit message if needed so it accurately describes the final state.
   - **Non-trivial change** (anything else):
     - Create a new commit with a full commit message.

2. **Generate commit message** – Commit messages must be generated in correct English perfect tense, but **without** using the word `has`.
   - **Perfect tense examples:**
     - ✅ "Added conversation_topic fallback to _identify_items"
     - ✅ "Fixed E402 import-order violations in debug scripts"
     - ✅ "Updated docstring to document fallback order"
     - ❌ "Add conversation_topic fallback" (imperative, not perfect tense)
     - ❌ "Has added conversation_topic fallback" (contains forbidden word "has")
     - ❌ "Adding conversation_topic fallback" (gerund, not perfect tense)

### After commit completion

Once the commit is complete:

1. **Post a Result report** – post a dated `yyyy-mm-dd Result:` section listing:
   - All updated files (code + docs).
   - New version number (if changed).
   - The final commit message.

2. **Ask the user** if they are satisfied using `ask_followup_question`. Do NOT use `attempt_completion` after commit. Instead, present the user with options to:
   - Review specific changes
   - Continue with a new task
   - Make additional changes

## Available slash commands

- `/dod-checklist` – runs the **Definition of Done Checklist**.
- `/commit-checklist` – runs the **Commit Checklist**.

## Test style

- Use `print()` for diagnostic output in tests, **not** `logging`/`logger`.
  `print()` is captured and shown by pytest's `-s` flag without any extra configuration.
  Logging output requires `--log-cli-level` and adds unnecessary complexity to test runs.
- `assert` statements are standard in pytest tests.

## Debugging workflow

When investigating a problem or bug, follow this iterative process **until the root cause is confirmed and fixed**:

1. **Form a hypothesis** – based on the error message, stack trace, or observed behaviour
2. **Do not modify code yet** – instead, propose a debugging approach to test the hypothesis
3. **Suggest debugging tools** – offer debug scripts, logging, breakpoints, or test cases to gather evidence
4. **Analyze the evidence** – review the results and determine if the root cause is proven
5. **If root cause is confirmed** – implement the fix with confidence
6. **If root cause is not confirmed** – refine the hypothesis and repeat steps 2–4

This iterative approach prevents blind fixes and ensures changes are targeted and effective. Never modify code based on unproven hypotheses.

## Safety and constraints

- Never remove or weaken security checks or validation logic without an explicit instruction and a clear justification.
- Search `tests/unit/` **and** `tests/integration/` for any test that references changed symbols,
  fields, or behaviour; update all affected tests. Every changed behaviour **must** have a
  corresponding test — do not skip this step.

## Error handling and silent failures

**Never implement silent error handling without explicit approval.**

When catching exceptions in code:

1. **Default non-silent behavior** – All caught exceptions must be handled explicitly:
   - Log the error with sufficient context for debugging
   - Re-raise the exception

2. **Silent pass prohibition** – Never use `except: pass` or `except Exception: pass` without:
   - A clear, documented reason why silent failure is acceptable
   - User approval obtained via `ask_followup_question`

3. **When proposing non-default error handling** – Use `ask_followup_question` to:
   - Explain the error handling approach you propose
   - Present alternatives (log and re-raise, log and return error status, silent pass)
   - Ask the user to choose and approve an alternative:
     - Log the error and re-raise it to the caller (i.e. always include the default non-silent behavior as a choice)
     - Log the error and return error status that the caller must handle (with explicit justification)
     - Log the error but pass/continue (with explicit justification)
     - Silent pass (with explicit justification)

4. **Non-exhaustive examples of silent-pass error handling that requires user approval:**
```python
# ❌ BAD – No logging, no context, no propagation
try:
    critical_operation()
except Exception:
    pass

# ❌ BAD – Silently returns None without logging or approval
try:
    return fetch_data()
except Exception:
    return None
```

## Python-specific rules

- Never run `ruff check --unsafe-fixes` unless explicitly instructed.
- Never disable ruff or pylint checks without asking first.
- Always place imports as recommended by ruff and pylint (stdlib → third-party → local, no reordering without linter approval).

### Continuous linting compliance during code generation

- All generated Python code should comply with ruff and pylint rules **before** being written to files
- This applies to all Python files in the project, including:
  - `/src` – main source code
  - `/tests` – test files (unit and integration)
  - `/debug` – debug scripts
  - `/experiments` – experimental code
  - `/utils` – utility scripts
  - Root directory – any `.py` files in the project root
  - Any other directories containing Python code
- Code generation should follow linting rules proactively, without requiring a separate `ruff check` or `pylint` run to fix issues
- Before generating code, check the **Lint and format** section defined in the DoD Checklist
- The goal is to generate clean, compliant code from the start, not to generate code and then fix it with linters
- If compliance conflicts with functionality, prioritize functionality and document the deviation with a comment explaining why the linting rule cannot be satisfied
- If a linting rule cannot be satisfied, ask the user before adding `# noqa` or `# pylint: disable` comments (see **Lint and format** section in the DoD Checklist for details)
