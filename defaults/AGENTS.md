## Efficiency defaults

- Minimize unnecessary model, context, and tool usage without compromising correctness or the requested outcome.
- Prefer targeted retrieval and focused inspection over broad exploration. Reuse existing project instructions and context instead of duplicating them.
- For routine execution and narrow delegated work, use the cheapest capable model or subagent when delegation is supported and materially useful; reserve GPT-6 Astra for difficult reasoning, complex judgment, or final verification that needs it.
- Keep successful tool results and progress updates brief. Include detailed diagnostics when something fails or remains unresolved.
- Preserve completed work, avoid repeating checks without a new reason, and keep final responses concise.
- Treat repeatable, specialized workflows as candidates for dedicated skills; do not create generic token-saving skills.

