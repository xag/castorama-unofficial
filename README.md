# castorama-unofficial

The wood panels Castorama France lists, as data for [furniture-design](https://github.com/xag/furniture-design). **Unofficial**: Castorama did not write or endorse it, and nothing here speaks for it.

## What is here

- **The range**: 729 products read from Castorama's public product sitemap (https://www.castorama.fr/fstrz/sm/sitemap-index.xml), each with its line, thickness, sheet size and address, in 23 lines (agglomere, contreplaque, contreplaque-okoume, contreplaque-peuplier, lamelle-colle-aulne, lamelle-colle-chene, lamelle-colle-hetre, lamelle-colle-pin, lamelle-colle-sapin, massif-acacia, massif-chene, massif-hetre, massif-pin, massif-sapin, massif-teck, mdf, mdf-hydrofuge, mdf-teinte, melamine, osb, osb-3, panneau-3-plis, panneau-fibres-dures). What a given store has in stock is not in the sitemap. A marketplace seller's product (/mkp/), sold and shipped by another firm, not in the shop's stores is left out.
- **The materials**: one per line and thickness (`materials/casto-<line>-<thickness>`), two for a board that bends differently along and across. [wood-panels](https://github.com/xag/wood-panels)'s `shops` module reads the titles and gives each line its values: a class's (P2, P3, MDF, OSB/3), a maker's board of the same type, or a species of furniture-design, all ungrounded unless the title names the class or the maker; the payload `shop` says what is sold and which board the values are.
- **The cutting service**: `tools/castorama-cutting-service`, a tool a part links `sawn_with`. Its page says: In every store, 'en fonction des magasins': plywood, MDF and HDF, OSB 3, particleboard and moisture-resistant particleboard, melamine-faced board, and forex (PVC); its FAQ says white melamine-faced board and, in some stores, plexiglas. Prices are given in store; a worktop cut is from 5 EUR a saw cut. The materials of the other lines are in its `refuses`. It gives no saw cut, depth or narrowest part, so furniture-design refuses a part sent to it until its cut is stated.

No kinds and no rules of its own: a part that `uses` one of these materials is judged by furniture-design's rules.

## Sources

The sitemap's entries as fetched on 2026-11-14 are kept in a private repo with the sha256 of each sitemap file, and `tests/test_values.py` checks that every product is an entry and reads as its row: clone that repo beside this one, or set `FURNITURE_REPO`, or that test fails and says why. `tools/read_range.py` reads the range again from a folder of sitemap files.

## Using it

```python
from furniture_design.knowledge import knowledge as general, merge
from wood_panels import knowledge as wood_panels
from castorama_unofficial import knowledge as castorama

tree.root.children = merge(general(), wood_panels(), castorama()) + [pieces]
```

## Design ledger

```sh
uv sync
uv run quern brief .
uv run quern check
```

There is no flight-recorder boundary: nothing here touches storage, the network, the clock or randomness at run time.

## Licence

- **The code** (`castorama_unofficial/*.py`, `tools/`, `tests/`, `ledger/`) is licensed under the [GNU Affero General Public License v3.0 or later](LICENSE), copyright 2026 Xavier Grehant.
- **The knowledge base**, the database `castorama_unofficial.knowledge()` returns (range.json and every value on its nodes), is licensed under [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0](LICENSE-DATA), database rights included, with one added permission: designing, building and selling furniture with it is allowed. An improvement is published here, through [CONTRIBUTING.md](CONTRIBUTING.md).
- Castorama's product names and sizes are cited from its sitemap, not licensed.

## Tests

`uv run pytest` runs the tests whose code, data or packages changed since they passed, last failures first then the fastest, under a time budget (testplan); `uv run pytest --all` runs them all, once a day. Both stop at the first failure.
