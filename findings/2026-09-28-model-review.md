# Model and compatibility review — 2026-09-28

Follow-up reviewed on 2026-10-05; the original dated observations remain below.

Optional maintenance reference, not additional always-loaded instructions.
No settings or installations are changed by this document.

## October 5 follow-up

The [official model guidance](https://learn.chatgpt.com/docs/models) now identifies
GPT-6.1 Sol as a near-Astra option for complex, repeated work; Astra remains the
most capable model. Evaluate 6.1 Sol as a stronger worker candidate where Luna is
insufficient, not as an automatic replacement for the owner's Astra lead.
Availability depends on plan, client and workspace controls; Work/Codex access
does not imply ordinary Chat access. A changed client default is not permission
to overwrite an explicit choice.

Choose reasoning separately: current guidance suggests the client's default for
6.1 Sol, High for Luna and Light for Astra as starting points, then adjust to the
task. Reasoning settings are not equivalent across generations. These are optional
evaluation baselines, not new mandatory worker presets or installation changes.

The [pricing page](https://learn.chatgpt.com/docs/pricing), checked October 5,
lists 6.1 Sol at the same input/output credit rates as 6 Sol and a lower cached-input
rate. This is not a guaranteed reduction in total task usage or included allowance.
It also distinguishes speed surcharges: Fast uses 2.5x included subscription
usage versus 2x purchased credits; Astra Ultrafast uses 8x versus 6x respectively,
relative to Standard for the same model. Eligibility varies. Leave speed settings
unchanged; do not enable a faster mode to save quota or treat billing multipliers
as speed measurements. Check live limits and the applicable billing surface.

The [retirement notice](https://learn.chatgpt.com/docs/changelog) still lists
October 14 for GPT-5.5 in ChatGPT/Work/Codex, not API. The previously proposed
authorized settings review remains relevant; this follow-up does not perform it.

These sources were opened on 2026-10-05. Reverify before applying; no new skill or
automatic synchronization is proposed.

## Worker candidates

The [official release notes](https://learn.chatgpt.com/docs/changelog) announce
GPT-6 Sol and Luna on September 22 for Work and Codex, subject to rollout and
workspace access, not ordinary Chat. Sol targets complex coding/agentic work;
Luna targets focused high-volume tasks. Verify the actual model picker and worker
controls before recommending a switch on an older installation.

The [current credit table](https://learn.chatgpt.com/docs/pricing), checked on
September 28, lists lower input, cached-input and output rates for GPT-6 Sol/Luna
than their GPT-5.6 counterparts. This supports evaluating them as worker candidates,
not promising task-level savings: reasoning, retries, context and verification
also consume usage. API dollar prices are not subscription quota percentages.

Recommendation: preserve the owner's best-available-lead policy (currently Astra).
Evaluate GPT-6 Luna for bounded routine work and Sol when workers need stronger
capability. Choose supported reasoning per task rather than automatically carrying
forward an old max/xhigh preset. Explicit user choices and local settings remain
unchanged until an authorized migration; do not rename or rewrite saved workers
merely because new models exist.

## Visual-task reevaluation

The [API changelog](https://developers.openai.com/api/docs/changelog) records a
September 25 image-encoding fix for GPT-6 Sol/Luna affecting API and Codex visual
tasks. Reconsider earlier negative visual evaluations where relevant. Rerun only
the affected checks within an authorized task and budget, not completed unrelated
work or side-effecting workflows automatically.

## Retirement and status checks

The [product changelog](https://learn.chatgpt.com/docs/changelog) also documents
GPT-5.5 retirement from ChatGPT, Work and Codex on October 14; API is unaffected.
During an authorized settings review, identify saved selections and propose a
compatible replacement. Do not silently alter an explicit user model choice.

New CLI usage analytics include token totals and skill/plugin activity. Use these
for targeted overhead investigations when available, but do not confuse activity
totals with remaining account allowance or assume every surface exposes them.

The original review sources were opened on 2026-09-28. Reverify availability, prices and retirement
status when applying these findings. No generic efficiency skill is warranted.
