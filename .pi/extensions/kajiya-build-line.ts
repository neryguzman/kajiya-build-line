// Kajiya Build Line local Pi extension.
// Portable rule: inspect the current working directory and never hard-code
// project-specific memory.

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function kajiyaBuildLineExtension(pi: ExtensionAPI) {
  pi.registerCommand("kajiya-build-line", {
    description: "Start a Kajiya backlog-governed build-line planning turn.",
    handler: async (_args, ctx) => {
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

      ctx.ui.notify("Kajiya Build Line prompt injected. The model should inspect the current repo before proposing work.", "info");

      // We use prompt injection into the chat turn rather than direct shell work.
      // The LLM runtime remains Pi/Pocock; this extension is only the handler.
      await ctx.sessionManager.addUserMessage?.(prompt);
    },
  });
}
