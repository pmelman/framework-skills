# framework-skills

A public, versioned dataset of **thinking frameworks rendered as applicable skills** —
each one a JSON document with the framework's distinctive claims, key vocabulary, an
executable analysis procedure, failure modes, canonical examples, and provenance.

The mission: increase the ability of humans *and* LLMs to find and apply a variety of
frameworks when thinking about problems. This repo is the product; apps, Claude skill
packs, and other frontends are consumers of it.

## Layout

```
index.json                       # manifest — the catalog consumers load first
schema/framework-skill.schema.json
skills/<slug>/v1.json            # immutable versions
skills/<slug>/latest.json        # copy of the newest approved version
scripts/generate_index.py        # regenerates index.json from the tree
scripts/validate.py              # schema + invariant validation (run in CI)
WISHLIST.md                      # frameworks worth authoring next
```

## Consuming the dataset

Both endpoints send `access-control-allow-origin: *`, so they work directly from a
browser:

```
# jsDelivr (CDN-cached; pin a tag for reproducibility — preferred)
https://cdn.jsdelivr.net/gh/pmelman/framework-skills@v0.1.0/index.json
https://cdn.jsdelivr.net/gh/pmelman/framework-skills@v0.1.0/skills/<slug>/latest.json

# raw GitHub (fallback)
https://raw.githubusercontent.com/pmelman/framework-skills/main/index.json
```

Load `index.json` first — name, description, and domains there are enough to render a
catalog and run recommendation. Fetch full skill JSON lazily, only for skills you apply.
`generated_at` in the manifest is your cache key; `skills/<slug>/vN.json` files are
immutable, so caching them forever is safe.

## Skill format

See [`schema/framework-skill.schema.json`](schema/framework-skill.schema.json) for the
authoritative definition, and
[`skills/bayesian-epistemology/latest.json`](skills/bayesian-epistemology/latest.json)
for the reference-standard example.

Current data is `schema_version: 2`. `schema_version: 3` adds `when_to_use: string[]` —
concrete, problem-first indicators that the framework applies ("you face a decision
under uncertainty with quantifiable evidence…"). New skills should target v3; the seed
catalog will be backfilled.

`review_status` is `"approved"` or `"needs_attention"` — the latter marks skills (often
agent-built) not yet human-reviewed; consumers should flag them visibly.

`relationships.*` entries are display names of other frameworks and may not resolve to
an existing skill. Dangling references are deliberate — like wiki redlinks, they mark
skills worth authoring (see [WISHLIST.md](WISHLIST.md)).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Every PR is validated in CI against the JSON
Schema, and `index.json` must be regenerated to match the tree.

## License

The dataset and everything else in this repo are licensed under
[CC BY 4.0](LICENSE). Attribution: "framework-skills contributors".
