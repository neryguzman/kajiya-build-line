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

export default function kajiyaBuildLineExtension(pi: ExtensionAPI) {
  const registerOnboard = (name: string) => {
    pi.registerCommand(name, {
      description: "Run Kajiya Build Line project onboarding/readiness discovery.",
      handler: async (_args, ctx) => {
        const prompt = onboardingPrompt();

        ctx.ui.notify(
          "Running kajiya_onboard_project. Read-only repo discovery prompt injected.",
          "info"
        );

        await ctx.sessionManager.addUserMessage?.(prompt);
      },
    });
  };

  registerOnboard("kajiya-onboard");
  registerOnboard("kajiya-build-line");
}
