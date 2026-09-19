# Best available lead within available usage

## Objective

Use the best available model to lead planning, orchestration, integration and final
review—currently GPT-6 Astra—while protecting every applicable usage limit.
Save usage through task-appropriate reasoning, focused context and cheaper capable
workers, not by routinely substituting a weaker lead.
Avoid exhaustion by reducing scope or saving progress and stopping before reserves
are threatened. Do not promise uninterrupted execution of every task.

This is advisory instruction, not an enforced quota controller. Shared concurrent
sessions, delayed readings, hidden limits and uncertain task cost prevent a guarantee
that an installation will never run out. Never claim to reserve account capacity.

## Read all available limits

For a simple current-status question, prefer the relevant authorized read-only
status capability and a direct answer. Avoid optional documentation research or
delegation unless the result is unclear or the user asks for an explanation.
Mandatory skill and higher-priority requirements still apply, including required
research. This is not permission to skip them or edit bundled skills. If live
access is unavailable, report that limitation; documentation cannot establish the
account's current usage, active model, task state or connection state.

Before substantial work, use the surface's read-only usage capability when available.
Check every reported window or bucket: five-hour, weekly, model-specific and any
other applicable limits. Interpret each using its reported unit and duration; do
not assume primary always means five-hour or secondary always means weekly.
For percentage-used readings, remaining is 100 minus usedPercent, clamped to 0–100.
Note each reset time and whether the allowance is shared. Never add percentages
across windows or assume spare capacity in one overrides a restriction in another.

Missing or unavailable data is unknown, not unlimited or zero usage. Say which
limits could not be verified. Ask for a current usage-panel reading if needed for
a substantial commitment; otherwise keep work bounded and explain the uncertainty.
Never bypass access controls to obtain usage information.

Use reported reset times for planning. Do not schedule artificial pings merely to
start a usage window; they consume resources and their benefit is not guaranteed.

## Select model and reasoning together

Keep the best available model as lead. Match its reasoning effort to difficulty,
ambiguity, consequences of error, context size and tool needs; strongest model
does not mean maximum reasoning for every task. Respect explicit user overrides.

Astra is the current lead recommendation, not a permanent model identifier.
Verify availability on the target surface; official API availability alone does
not establish ChatGPT/Codex account access. Review future candidates against
current evidence. Select cheaper capable workers such as Luna for bounded work.
Delegate only when expected savings exceed coordination overhead;
consider total lead and worker usage and limit concurrency when reserves are tight.
Do not assume a model switch provides a separate allowance or lower usage cost.
Verify current availability and documented cost/limit behavior before relying on it.

Respect explicit user model choices and local permissions. If the active surface
cannot switch models/reasoning, recommend the appropriate choice and ask the user
to change it; never claim a switch occurred. If allowance is insufficient, explain
the tradeoff and ask before downgrading the lead or reducing scope. Save progress
and stop safely while awaiting the decision; do not silently sacrifice correctness.

## Budget, recheck and stop safely

Honor the user's budget and reserve for every applicable limit. Without a stated
reserve, explain a conservative working reserve and bounded plan before substantial
execution; ask for a decision if no defensible plan fits. Reserves are planning
margins, not guaranteed quota allocations or exact predictions of consumption.

Account for both short-term headroom and time until longer-window resets. A weekly
balance should not be spent merely because the five-hour window has room. Leave
headroom for final verification, saving progress and other concurrent sessions.

For each reported window, consider how long the remaining allowance must last.
When both remaining allowance and a future reset time are known, estimate a
sustainable pace: max(0, remaining allowance minus working reserve) divided by
time until reset. For percentages, express the result in percentage points per
hour or day, not a percentage of the remaining balance. Use a suitable unit for
short windows and treat each window separately; never invent a missing window.

Illustration only: 91 percentage points remaining over 6 days 22 hours is about
13.2 points per day, or 11.7 with a 10-point reserve. These are not account readings,
a default reserve, a daily product limit or a guaranteed spending budget.

Allow for expected upcoming work and all sessions sharing the allowance. Compare
recent consumption with the sustainable pace only when readings cover the same
bucket and reset period; do not attribute shared consumption solely to this task.
Recalculate after resets or material changes. If reset time or readings are absent,
report that pacing is unknown rather than fabricate an estimate. A heavy day may
be offset by lighter later work, but ask before changing scope or the lead model.

Recheck at meaningful milestones, before expensive phases or delegation, and after
unexpected retries or scope growth. Increase checking frequency as headroom shrinks;
avoid polling after every trivial action. Use observed consumption as an estimate,
not a guarantee. Stop retry loops that are not producing useful new evidence.

If any relevant limit approaches the working reserve, do not launch another
expensive phase. Offer a cheaper capable approach, smaller scope, or deferral until
reset. Save a concise local handoff with completed work, evidence, remaining work,
next step and latest known limits. Report what remains and end the work cleanly;
do not create an automatic resumption unless separately requested.

Never buy credits, redeem resets, change spending controls, switch accounts or
workspaces, or bypass limits without appropriate explicit authorization. Never
restart completed work merely because a new session or reset became available.

## Keep context useful

Start from the user's relevant files, error, desired result and acceptance criteria;
expand inspection only when the evidence requires it. Keep stable preferences short
and project details in their project. Do not copy this whole policy into every
instruction file or remove existing preferences merely to shorten them.

Incorporate user corrections promptly where the surface supports steering. Keep
successful tool output focused on results and evidence; retain enough failure
diagnostics to investigate correctly. Brevity must not hide uncertainty or failures.

When relevant, review unused plugins and tool context, explain the tradeoff, and
ask before disabling anything. Do not assume every integration has the same cost.
Use images when they are needed for the task, not as a substitute for available text.
