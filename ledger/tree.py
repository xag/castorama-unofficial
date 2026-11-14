"""The decisions castorama-unofficial is bound by, as a ledger. Read it with `uv run quern brief .`, never whole.

Vocabulary: ledger@0.8.0 and grounding@1.2.0, pinned in quern.lock.
"""

from __future__ import annotations

import os
from pathlib import Path

import quern.grounding  # noqa: F401
from quern import Node, Quern
from quern.library import consume

OWNER = "Tu feras aussi un Norpaneau unofficial ainsi que pour les autres chaines"


def _alt(id_: str, name: str, why: str) -> Node:
    return Node(id=id_, kind="alternative", name=name, payload={"why": why})


def entries() -> list[Node]:
    return [
        Node(
            id="the-range-is-read-from-the-public-sitemap", kind="decision",
            name="Castorama's range is what its public product sitemap lists (https://www.castorama.fr/fstrz/sm/sitemap-index.xml), read by wood_panels.shops: "
                 "every product whose title or address states a board, its line and three sizes; the entries are kept "
                 "privately with the sha256 of each sitemap file. What a given store has in stock is not in it"
                 " ; " + "a marketplace seller's product (/mkp/), sold and shipped by another firm, not in the shop's stores is left out",
            payload={"decided_on": "2026-11-14", "the_owner": OWNER,
                     "why": "The sitemap is what the shop publishes for robots; its titles state the boards' sizes."},
            children=[_alt("the-product-pages", "Read each product page",
                           "One request per product for what the sitemap already states.")],
        ),
        Node(
            id="the-cutting-service-is-what-its-page-says", kind="decision",
            name="Castorama's cutting service is tools/castorama-cutting-service, a tool a part links sawn_with, stating only "
                 "what its page says (the boards it cuts; it refuses the rest); "
                 "it states no cut, depth or narrowest part, which the page does not give",
            links={"rests_on": ["the-range-is-read-from-the-public-sitemap"]},
            payload={"decided_on": "2026-11-14", "the_owner": OWNER,
                     "why": "A part sent to the service is judged by what the service says it does; what it does not "
                            "say is left for a person to ask in the store."},
            children=[_alt("assume-a-panel-saws-rules", "Give it a panel saw's usual cut and narrowest part",
                           "Figures the shop never gave, printed as its own.")],
        ),
    ]


def build() -> Quern:
    root = Path(__file__).resolve().parents[1]
    lib, refs = consume(root, os.environ.get("QUERN_REGISTRY", root.parent / "quern-registry"))
    quern = Quern(packages=list(refs))
    quern = lib.effective(quern)
    quern.root.children = entries()
    return quern
