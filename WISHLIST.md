# Wishlist — frameworks worth authoring

Two feeds: **priority domains** (current catalog is philosophy/religion-heavy; these
broaden coverage) and **dangling references** (frameworks the existing skills already
cite in `relationships.*` but that don't exist in the catalog yet — demand measured in
references). Regenerate the dangling list anytime with:

```
python scripts/validate.py --dangling
```

## Priority domains

### Decision & strategy
- OODA Loop
- Cynefin
- Theory of Constraints
- Expected-Value Reasoning
- Red Teaming
- Pre-mortem / Prospective Hindsight

### Systems & engineering
- Systems Thinking
- First-Principles Reasoning
- TRIZ
- Feedback Loops / Control Theory thinking
- Antifragility

### Science & evidence
- Causal Inference (Pearl)
- Fermi Estimation
- Strong Inference (Platt)
- Replication / Robustness thinking

### Social & organizational
- Double-Loop Learning
- Jobs-to-be-Done
- Chesterton's Fence
- Overton Window
- Principal–Agent analysis

### Psychology & rationality
- Dual-Process Theory
- Cognitive Behavioral framing
- Inversion
- Goodhart's Law

## Most-referenced dangling relationships

As of the v0.1.0 seed (50 skills, 162 dangling names total; ≥2 references listed):

- **Systems Thinking** (13 references) — also a priority domain
- **First Principles** (11 references) — also a priority domain
- **Stoicism** (9 references)
- **Classical Logic** (4 references)
- **Contextualism in epistemology** (3 references)
- **Chesterton's Fence** (2 references) — also a priority domain
- **Contractarianism** (2 references)
- **Formal Learning Theory** (2 references)
- **Knowledge-first epistemology (Williamson)** (2 references)
- **Logical Positivism** (2 references)
- **Moral Sentimentalism** (2 references)
- **Rationalism** (2 references)
- **Utility Theory** (2 references)

## Backfill

- All 50 seed skills need `when_to_use` (problem-first indicators) added and a bump to
  `schema_version: 3`.
