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


function builderPlanPrompt(issueId: string): string {
  return `
You are executing pi.dev kajiya_builder_patch_plan inside Kajiya Build Line.

Role:
- Produce a bounded implementation plan for a selected backlog issue.
- Do not modify files.
- Do not create code.
- Do not run external writes.
- Do not use direct Gemini SDK.
- Use Pi/Pocock as the LLM runtime.
- Use local project files as memory.
- Do not rely on previous chat memory.

Selected issue_id:
${issueId}

Before planning, inspect read-only evidence:

1. Run: kajiya-build-line status
2. Run: kajiya-build-line qa
3. Read: docs/state/backlog.json
4. Read: docs/state/current-project.json
5. Read: docs/pi-devs/kajiya_builder_patch_plan.md
6. Read relevant schemas under docs/schemas/

Return JSON-compatible output with:
- schema_version: "kajiya.builder_patch_plan.v1"
- kind: "kajiya_builder_patch_plan"
- ok
- pi_dev_id: "kajiya_builder_patch_plan"
- runtime_status
- issue_id
- objective
- evidence_read
- missing_evidence
- proposed_change_type
- files_likely_to_change
- implementation_plan
- validation_commands
- risks
- requires_human_approval
- next_safe_actions

Rules:
- Plan-only.
- If git is dirty, return runtime_status "blocked_dirty_worktree".
- If QA fails, return runtime_status "qa_failed".
- If issue_id is missing or not found, return a blocking status.
- Do not claim files were changed.
- Do not close issues.
- Do not commit.
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

  pi.registerCommand("kajiya-builder-plan", {
    description: "Prepare a bounded Kajiya Builder patch plan prompt for a selected issue.",
    handler: async (args, ctx) => {
      const rawArgs = Array.isArray(args) ? args.join(" ") : String(args || "");
      const match = rawArgs.match(/(?:issue_id=|--issue-id\s+)([A-Za-z0-9._-]+)/);
      const issueId = match?.[1] || rawArgs.trim() || "KBL-005";

      const prompt = builderPlanPrompt(issueId).trim();
      ctx.ui.setEditorText(prompt);
      ctx.ui.notify(
        `kajiya_builder_patch_plan prompt for ${issueId} is now in the editor. Press Enter to run it.`,
        "info"
      );
    },
  });
}
