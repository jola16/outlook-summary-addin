# Completion and follow-up behavior

When deciding how to wrap up or pause a task, choose between
`attempt_completion` and `ask_followup_question` as follows:

- Use `attempt_completion` only when:
   - The current task is fully complete (not just a subtask or intermediate step).
   - All required changes have been committed according to the conventions
     and instructions defined in `general.md` (including tests, formatting,
     DoD and commit requirements).
  - You want to present a brief result summary and then optionally let the
    user decide what to do next.

- Use `ask_followup_question` when:
  - You need the user to choose between multiple valid next steps.
  - You need clarification, preferences, or additional information to proceed.
  - You want to present interactive next-step options as buttons via the
    `follow_up` parameter.

## attempt_completion behavior

When using the `attempt_completion` tool:

- Keep all output minimal and focused on completion.
- Include at most one short sentence summarizing what was completed.
- Do not list internal actions, tools used, or implementation details.
- Only invoke `attempt_completion` after the entire task is complete and
   committed according to `general.md` (never for partial or in-progress work).
- After the brief summary:
  - Optionally mention that the task has been completed and committed.
  - Ask the user, in plain text, if they are ready to proceed or start a new task.
  - Optionally ask the user if they would like a more detailed summary.

## ask_followup_question behavior

When using the `ask_followup_question` tool:

- Ask a single, clear question about how to proceed or what is needed to continue.
- Always populate the `follow_up` parameter with 2–4 short next-step options
   (for example: run tests, review key changes, continue the DoD flow,
   start the commit process or request a more detailed summary, in line with
   the conventions and requirements defined in `general.md`).
- Ensure the `follow_up` options match what you would otherwise list as
  next steps in plain text.

