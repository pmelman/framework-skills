# Contributing a framework skill

Skills are data. Adding or improving one is a docs-style contribution: a PR that adds
or edits JSON under `skills/`, validated automatically by CI.

## Adding a new skill

1. Pick the framework (check [WISHLIST.md](WISHLIST.md) for wanted ones) and confirm it
   isn't already in `index.json` under another name.
2. Compute the slug: lowercase the name, replace every non-alphanumeric run with `-`,
   trim leading/trailing `-` (e.g. "Occam's Razor" → `occam-s-razor`).
3. Create `skills/<slug>/v1.json` conforming to
   [`schema/framework-skill.schema.json`](schema/framework-skill.schema.json), and copy
   it to `skills/<slug>/latest.json`.
4. Regenerate the manifest: `python scripts/generate_index.py`.
5. Validate locally: `pip install jsonschema && python scripts/validate.py`.
6. Open a PR.

## Improving an existing skill

Never edit a published `vN.json` — versions are immutable (consumers cache them
forever). Instead:

1. Copy the current latest to `v<N+1>.json`, make your changes there, and bump the
   `version` field to match.
2. Overwrite `latest.json` with the new version.
3. Regenerate the manifest and validate (steps 4–5 above).

## Quality bar (enforced in review)

- **`core_claims` are distinctive and falsifiable-ish.** No platitudes a rival
  framework would also assert. If Stoicism and Utilitarianism would both happily sign a
  claim, it doesn't belong in either.
- **`operative_procedure` is executable.** A model given only the skill should produce
  a recognizably framework-shaped analysis.
  [`skills/bayesian-epistemology`](skills/bayesian-epistemology/latest.json) is the
  reference standard.
- **`canonical_examples` come from real sources** — never invented.
- **`relationships.rivals` is populated.** Downstream synthesis depends on knowing
  where frameworks genuinely disagree. Entries are display names; it's fine (good,
  even) if they don't resolve to existing skills yet — dangling references seed the
  wishlist.
- **`when_to_use` is written problem-first** (schema_version 3): describe the *problem
  indicators* ("you face a decision under uncertainty with quantifiable evidence…"),
  not the framework. This is what recommendation matches against.
- **`source_texts` cite real sources** with `kind` ∈ primary/secondary/tertiary.
- **Agent-authored skills land as `review_status: "needs_attention"`** until a human
  has reviewed them. Set `"approved"` only after human review.

## PR checklist

- [ ] `python scripts/validate.py` passes locally
- [ ] `python scripts/generate_index.py` run; `index.json` committed
- [ ] New versions added as new `vN.json` files; no published version edited
- [ ] `latest.json` matches the highest `vN.json`
- [ ] `core_claims` pass the rival-framework test
- [ ] `canonical_examples` traceable to a source
- [ ] `review_status` honest about review state

## Licensing

By contributing you agree to license your contribution under
[CC BY 4.0](LICENSE).
