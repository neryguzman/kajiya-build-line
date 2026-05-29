// Kajiya Build Line local Pi extension.
// This extension is portable: it must inspect the current working directory
// and must not hard-code any project-specific memory.

export default function extension(api: any) {
  api.commands.register({
    name: "kajiya-build-line",
    description: "Inspect current repo and start a Kajiya backlog-governed build-line planning turn.",
    handler: async () => {
      const prompt = `
You are running Kajiya Build Line inside Pi.

Do not rely on previous chat memory.
Inspect the current working directory as the project root.
Before proposing implementation, gather evidence from local files where present:

1. .kajiya/project.json
2. docs/state/current-project.json
3. docs/state/backlog.json
4. docs/LLM_HANDOFF_PROTOCOL.md
5. git status --short
6. git --no-pager log --oneline -12

Then report JSON-compatible output with:
- ok
- runtime_status
- project_root
- evidence_read
- missing_evidence
- inferred_project_type
- active_backlog_candidates
- next_safe_actions

Rules:
- Do not modify files.
- Do not create code yet.
- Do not use global memory.
- Do not assume this is kajiya-context-engine.
- If no backlog exists, recommend initializing one.
- If a backlog exists, identify candidate issue_ids but require human selection before implementation.
`;
      await api.chat.send(prompt);
    },
  });
}
