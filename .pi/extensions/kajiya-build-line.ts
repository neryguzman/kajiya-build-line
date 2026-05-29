// Kajiya Build Line local Pi extension.
// Portable rule: inspect the current working directory and never hard-code
// project-specific memory.

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

function onboardingPrompt(): string {
  return `
You are executing pi.dev kajiya_onboard_project inside Kajiya Build Line.

Role:
- Discover the current repository.
- Determine whether it is ready for backlog-governed work.
- Do not modify files.
- Do not create code.
- Do not rely on previous chat memory.
- Do not assume this is kajiya-context-engine.

Inspect the current working directory as the project root.

Gather evidence from local files/commands where present:

1. .kajiya/project.json
2. docs/state/current-project.json
3. docs/state/backlog.json
4. docs/LLM_HANDOFF_PROTOCOL.md
5. git status --short
6. git --no-pager log --oneline -12

Return JSON-compatible output with:
- ok
- pi_dev_id: "kajiya_onboard_project"
- runtime_status
- project_root
- evidence_read
- missing_evidence
- inferred_project_type
- active_backlog_candidates
- next_safe_actions

Rules:
- Read-only.
- No file modifications.
- No external writes.
- No global/project-crossing memory.
- If no backlog exists, recommend initializing one.
- If a backlog exists, identify candidate issue_ids but require human selection before implementation.
- If project identity is missing, recommend initialize_project_profile.
`;
}


function builderContextPrompt(issueId: string): string {
  return `
You are executing pi.dev kajiya_builder_context inside Kajiya Build Line.

Role:
- Prepare bounded Builder context from an existing human-authored task brief.
- Do not invent strategy.
- Do not invent roadmap.
- Do not invent backlog items.
- Do not create an implementation plan.
- Do not modify files.
- Do not create code.
- Do not commit.
- Do not push.
- Do not close issues.
- Do not rely on previous chat memory.

Selected issue_id:
${issueId}

Deterministic source of truth:
- docs/task-briefs/${issueId}.json
- docs/state/current-project.json
- docs/state/backlog.json
- kajiya-build-line checkpoint
- kajiya-build-line backlog
- kajiya-build-line qa
- kajiya-build-line validate-json

Before preparing context, inspect read-only evidence:

1. Run: kajiya-build-line checkpoint
2. Run: kajiya-build-line backlog
3. Run: kajiya-build-line qa
4. Run: kajiya-build-line validate-json
5. Read: docs/task-briefs/${issueId}.json
6. Read evidence paths referenced by the task brief if present.
7. Read allowed_files from the task brief only if needed for context.

Return JSON-compatible output with:
- schema_version: "kajiya.builder_context.v1"
- kind: "kajiya_builder_context"
- ok
- pi_dev_id: "kajiya_builder_context"
- runtime_status
- issue_id
- task_brief_path
- evidence_read
- missing_evidence
- allowed_files
- forbidden_actions
- validation_commands
- bounded_builder_context
- next_safe_actions

Rules:
- Context-only.
- Do not produce a strategic plan.
- Do not propose a roadmap.
- Do not propose new backlog items.
- Do not claim files were changed.
- If git is dirty, report it but do not fix it.
- If QA fails, report it but do not fix it.
- The human/operator owns the plan.
- The Builder may later implement only the human-authored task brief.
`;
}

export default function kajiyaBuildLineExtension(pi: ExtensionAPI) {
  const registerOnboard = (name: string) => {
    pi.registerCommand(name, {
      description: "Prepare Kajiya Build Line project onboarding/readiness discovery.",
      handler: async (_args, ctx) => {
        const prompt = onboardingPrompt().trim();

        ctx.ui.setEditorText(prompt);

        ctx.ui.notify(
          "kajiya_onboard_project prompt is now in the editor. Press Enter to run it.",
          "info"
        );
      },
    });
  };

  registerOnboard("kajiya-onboard");
  registerOnboard("kajiya-build-line");

  const registerBuilderContext = (name: string, deprecated = false) => {
    pi.registerCommand(name, {
      description: deprecated
        ? "Deprecated alias for /kajiya-builder-context. Prepares bounded Builder context."
        : "Prepare bounded Kajiya Builder context from a human-authored task brief.",
      handler: async (args, ctx) => {
        const rawArgs = Array.isArray(args) ? args.join(" ") : String(args || "");
        const match = rawArgs.match(/(?:issue_id=|--issue-id\s+)([A-Za-z0-9._-]+)/);
        const issueId = match?.[1] || rawArgs.trim() || "KBL-025";

        const prompt = builderContextPrompt(issueId).trim();
        ctx.ui.setEditorText(prompt);
        ctx.ui.notify(
          `${name} context prompt for ${issueId} is now in the editor. Press Enter to run it.`,
          deprecated ? "warn" : "info"
        );
      },
    });
  };

  registerBuilderContext("kajiya-builder-context");
  registerBuilderContext("kajiya-builder-plan", true);
}
