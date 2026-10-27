# One-row visual worker instructions

This full pet style replacement is authorized. Parent uses work-pets:update-pet, create-pet's mandated generation/validation pipeline, and imagegen. You own ONLY the assigned row. Do not create or update the pet. No other files except that row and its QA/prompt records.

RUN = [local path redacted]
PYTHON = [local path redacted]
SCRIPTS = [local path redacted]

Read the assigned generated prompt prompts/rows/STATE.md and imagegen-jobs.json's matching inputs. Inspect canonical-base and the matching layout guide before generation with view_image. Base is approved: clean Japanese anime cel character, sharp charcoal ink outlines, clean flat fills with minimal shading, NO fur/grunge/pencil texture. Canonical-base has authority for NEW style; original fetched sheet and old screenshot are identity/motion references only. Preserve charcoal beanie with mustard cuff, same scarf/teal jacket with small pale hem accents, green attached satchel screen-left in frontal pose, ringed tail screen-right, worried round dark eyes in dark masks. No detached tears, sweat icons, white border, labels or copied layout lines.

Use built-in image_gen exactly once initially with generated prompt plus assigned motion notes. Attach ALL FOUR refs: references/canonical-base.png, stored-original.png, references/reference-02.png, references/layout-guides/STATE.png. Give initial functions.exec yield_time_ms 120000, then wait only on returned cell ID. Keep tool output concise; show generatedImage(result), don't print base64. Tool returns output_hint containing local generated path; copy selected PNG to decoded/STATE.png, preserving default original. Save supplemented actual prompt to prompts/actual-STATE.md.

Immediately run extract_strip_frames.py --decoded-dir RUN/decoded --output-dir RUN/qa/rows/STATE/frames --states STATE --method auto, then inspect_frames.py --frames-root RUN/qa/rows/STATE/frames --json-out RUN/qa/rows/STATE/review.json --states STATE --require-components. Visually check source or frame strip: correct count and facing, consistent identity/size, all complete poses separated, baseline stable except jump lift, no loose effects, same arm throughout wave. If only extraction/layout fails, return exact failure promptly; parent handles deterministic correction. Regenerate only an obvious genuine source failure, at most one targeted retry. Never fake a successful report.

Return selected source path, QA ok/fail, concise visible evidence. No long investigation, no package install, no final atlas assembly. Parent handles shared scaling, registration, edge cleanup and all final checks.
