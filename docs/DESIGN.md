# Design: the simulation engine and where its rules come from

This document describes what the code in `index.html` actually does, the parameters you can tune, and which research finding motivates each rule.

## Actors

**Brand agent.** Holds a mandate parsed from the brief. Allocates budget across creators, opens offers, trims packages that cannot fit, trades flat fee for commission uplift, closes gaps, and walks away with a logged reason.

**Creator agents (four).** Each holds a private profile: followers, engagement, affinity with the brand (derived from prior orders), per-deliverable floors, a content bank, an hourly floor for new content, and a standing policy. Each proposes a package, counters by a configured patience, and never goes below its floor.

**LTK referee.** Deterministic. Validates every brand offer against the creator's floor before it reaches the creator agent, verifies the final deal against floor and max-share rules, records signatures, and mints attribution links.

## World model

| Symbol | Value | Meaning |
|---|---|---|
| `AOV` | $142 | Average order value |
| `COMM` | 12% | Base commission rate |
| `PATIENCE` | 0.72 | Fraction of the ask-to-floor gap a creator agent keeps each round |
| `reach` | IG post 0.55 · TT story 0.22 · Reel 0.90 | Share of followers reached |
| `click` | 0.18 | Click-through among engaged viewers |
| `hours` | IG post 1.5 · TT story 0.4 · Reel 2.5 | Human time for new content |

Projections per deliverable:

```
clicks  = followers × reach × engagement × click
orders  = clicks × 0.02 × (0.5 + affinity)
comm    = orders × AOV × (COMM + uplift)
```

## Mandate parsing

From the brief text: audience (`women` → "Women 25–40"), channels (`instagram`, `tiktok`), `reel` requirement, deadline (`N days`), and affinity weight (0.8 if the brief says "already sold" or "prefer creators who", else 0.4). Fixed policy: max 60% of budget to one creator, walk if cost per projected order at floor exceeds $95, human approval flag for any single deal over 75% of budget.

## Allocation

```
score_i = followers × engagement × (1 − w + 2·w·affinity)      w = affinity weight
alloc_i = min(0.6 × budget, budget × score_i / Σ score)
```

## Creator package construction

1. Enumerate candidates: every relevant bank asset, plus up to three "new" slots per type **only if** `floor × 1.35 + projected commission − hourly × hours > 0`.
2. Sort bank-first, then by projected commission per ask dollar.
3. If the mandate requires a reel and the creator's reel floor is at most 70% of allocation, add a reel first.
4. Add candidates while the package **floor** stays within allocation (caps: 2 IG posts, 3 stories, 1 reel). The **ask** is 1.35 × floor; the package is sized to floors, the price is anchored above.

## Negotiation protocol

**Fit phase.** Brand opens at `min(alloc, 0.72 × ask)`. If below floor, the referee blocks it. If the floor fits within `alloc × 1.05`, the brand moves to floor. Otherwise the brand proposes dropping the weakest item (never the last item of a required channel or the required reel if anything else can go), the creator re-prices at 0.95 × remaining asks, and the loop repeats. After two trims, or if only one item remains, or if cost per projected order at floor exceeds the mandate ceiling, the brand walks.

**Rounds (max six).**

- Round 1 with affinity ≥ 0.7: brand offers +2 pts commission uplift and shaves the flat 4%.
- Creator values uplift at `projected commission × (uplift / COMM) × 0.6` (risk-discounted against cash).
- Creator accepts if `offer + uplift value ≥ 0.97 × ask`, or its next counter would be within 3% of the offer, or the brand is at its ceiling (`alloc × 1.05`) and the gap is under 12%.
- Otherwise creator counters at `max(floor, ask − (ask − floor) × (1 − PATIENCE) − 0.6 × uplift value)`.
- Brand closes 55% of the remaining gap, capped at its ceiling.

**Final verification.** Referee checks flat ≥ floor and share ≤ 60%, records both signatures, mints one attribution link per deliverable.

## Execution

Bank items schedule immediately, one per day starting day 2 + creator index. New items are grouped by type into one batched human ask showing `fee share + projected commission − hours × hourly = net`. In the simulation the human taps Yes after a delay; the real product would wait.

## Ledger

Thirty compressed days. Each live deliverable emits clicks on a decaying curve from its projected total, orders by `0.02 × (0.5 + affinity)`, and commission per order at the deal's rate. Flat fee shares release on go-live. About 28% of orders are flagged as completed by the shopper's personal agent with a verified credential. After day 30 the unspent budget releases as a bonus to the creator with the most orders.

## Research mapping

| Rule in the prototype | Finding | Source |
|---|---|---|
| Typed offers; referee blocks sub-floor offers; profit verification before settlement | Baseline models accept individually irrational (money-losing) contracts in 19.2% of negotiations vs 0–0.6% for stronger tiers; automated profit verification is the binding guardrail | Liang & Xu, *When LLM Agents Negotiate: Private Information and Dynamic Bargaining in Supply Chains* (2026) |
| Same policy and the same `PATIENCE` on both sides; LTK sets it | Prompted strategic patience explains ~90% of surplus-division variance; provider identity shifts surplus 7–30 pts; vendor and configuration choice is a distributional decision | Liang & Xu (2026) |
| One brand agent negotiates with all creators in parallel; explicit allocation strategy | Deal quality improves with more buyers and sellers (liquidity); all frontier models show a systematic buyer disadvantage | Liu, Gu & Song, *AgenticPay* (2026) |
| Settle in 2–4 rounds; ceiling detection to avoid "last-mile" stalls | Frontier models reach 100% deal rate in ~4 rounds; weaker models time out within $5 of agreement | *AgenticPay* (2026) |
| Content bank first; batched human asks with EV math | Agents reduce transaction costs by converting search, quoting, scheduling into compute; demand for agents is derived demand (effort reduction vs decision quality) | Shahidi, Rusak, Manning, Fradkin & Horton, *The Coasean Singularity?* NBER w34468 (2025) |
| Creator agent policy set once; agent exposed to any host | Bring-your-own vs platform-provided ("bowling-shoe") agents; horizontal vs vertical specialization | *Coasean Singularity* (2025) |
| Attribution credential per click; commission survives agent checkout | Delegation tokens with scope, expiry, and audit endpoints; agents verifiably acting for a specific human | South et al., *Authenticated Delegation and Authorized AI Agents* (2025); Personal Agent Protocol (Poppy) draft 0.3 (2026) |
| Human feedback and purchase outcomes as the scarce asset; walk-aways logged for re-bid | Shift from attention economy to preference economy; service agents designed for agent-to-agent interaction | Rothschild et al., *The Agentic Economy* (2025) |

## Known simplifications

- One brand, four creators, three deliverable types, no exclusivity or usage-rights terms.
- Humans always say yes in the simulation.
- No real posting, payments, or identity. The "credential" is a counter.
- Deterministic seed (`mulberry32(7)`), so identical inputs reproduce identical runs.
