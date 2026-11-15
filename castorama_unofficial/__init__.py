"""The wood panels Castorama France lists, as data on furniture-design's kinds (source, clause, material, tool),
each line read as a board of wood-panels. Unofficial: Castorama neither wrote nor endorsed it.

What the shop lists comes from its public product sitemap (range.json, read by tools/read_range.py from the
sitemap files as fetched): every product whose title or address states a board, its line, thickness and sheet
size. Each is a clause under sources/castorama-sitemap. wood_panels.shops reads the titles and makes the materials:
one per line and thickness, `casto-<line>-<thickness>`, its payload `shop` saying what is sold and which
board its values are. A marketplace seller's product (/mkp/), sold and shipped by another firm, not in the shop's stores is left out.

    from furniture_design.knowledge import knowledge as general, merge
    from wood_panels import knowledge as wood_panels
    from castorama_unofficial import knowledge as castorama
    tree.root.children = merge(general(), wood_panels(), castorama()) + [pieces]
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from quern.tree import Node
from furniture_design.knowledge import with_authority
from wood_panels import shops

HERE = Path(__file__).parent
SHOP = "Castorama"
PREFIX = "casto"
SOURCE = "castorama-sitemap"


@lru_cache(maxsize=1)
def rows() -> list[dict]:
    return json.loads((HERE / "range.json").read_text(encoding="utf-8"))


SERVICE = "castorama-cutting-service-page"


def service_page() -> Node:
    """The page where Castorama describes its cutting service: what it says, by locator, in our words."""
    return Node(id=SERVICE, kind="source", name="Castorama France, its cutting service (https://www.castorama.fr/services/decoupe)",
                payload={"publisher": "Castorama France", "year": 2026, "url": "https://www.castorama.fr/services/decoupe", "fetched": "2026-11-14",
                         "sha256": "e0015051df502b76bf0030c95ca806425e025f1410b700e6878110f0e2b67687", "licence": "copyrighted",
                         "capture": "private copy, identified by its sha256"},
                children=[Node(id="what-it-cuts", kind="clause",
                               payload={"locator": "the page's description of the service",
                                        "in_our_words": "In every store, 'en fonction des magasins': plywood, MDF and HDF, OSB 3, particleboard and moisture-resistant particleboard, melamine-faced board, and forex (PVC); its FAQ says white melamine-faced board and, in some stores, plexiglas. Prices are given in store; a worktop cut is from 5 EUR a saw cut."})])


def cutting_service() -> Node:
    """Castorama's cutting service as a tool a part links sawn_with: the boards it does not cut, as its page says.
    It states no cut, no depth and no narrowest part, which its page does not give."""
    refuses = [f"materials/{m.id}" for m in shops.materials(PREFIX, SHOP, f"sources/{SOURCE}", rows())
               if not m.payload["shop"]["line"].startswith(('contreplaque', 'mdf', 'osb', 'agglomere', 'melamine'))]
    return Node(id="castorama-cutting-service", kind="tool", name="Castorama's cutting service",
                payload={"maker": "Castorama France", "saw_kind": "panel saw",
                         "does": "cuts the panels the store sells to the customer's sizes, in straight cuts",
                         "unverified": "the service and what it cuts depend on the store, its page says"},
                links={"per": [f"sources/{SERVICE}/what-it-cuts"], "refuses": refuses})


# Who stands behind each source (furniture-design's AUTHORITIES).
AUTHORITY = {
    "castorama-cutting-service-page": "maker",
}


def knowledge() -> list[Node]:
    """The branches to merge beside furniture-design's and wood-panels's: the sources, the materials and the cutting service."""
    out = shops.knowledge(PREFIX, SHOP, SOURCE, "Castorama France, product sitemap (https://www.castorama.fr/fstrz/sm/sitemap-index.xml)",
                          "https://www.castorama.fr/fstrz/sm/sitemap-index.xml", "2026-11-14", rows())
    out[0].children = with_authority(out[0].children + [service_page()], AUTHORITY)
    out.append(Node(id="tools", kind="", children=[cutting_service()]))
    return out
