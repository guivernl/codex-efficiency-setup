## Efficiency defaults

- Minimize unnecessary model, context, and tool usage without compromising correctness or the requested outcome.
- Prefer targeted retrieval and focused inspection over broad exploration. Reuse existing project instructions and context instead of duplicating them.
- Before a substantial Work/Codex task, read the current shared usage limits through the app's read-only usage capability when available. Calculate remaining allowance from the reported usage, note the reset time, and plan proportionately. Never redeem a reset credit, purchase credits, or change spending controls without explicit user confirmation.
- Use GPT-6 Astra as the lead planner, orchestrator, integrator, and final reviewer. Delegate narrow, bounded execution to GPT-5.6 Luna when model-selectable subagents are supported and the expected saving exceeds coordination overhead. Keep difficult reasoning and judgment with Astra.
- Work within any usage budget the user provides. When no budget is provided, choose a conservative execution plan based on the verified remaining allowance; do not invent or promise an exact consumption percentage.
- Keep successful tool results and progress updates brief. Include detailed diagnostics when something fails or remains unresolved.
- Preserve completed work, avoid repeating checks without a new reason, and keep final responses concise.
- Treat repeatable, specialized workflows as candidates for dedicated skills; do not create generic token-saving skills.
