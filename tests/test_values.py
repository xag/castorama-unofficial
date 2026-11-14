"""The range against the sitemap entries it was read from, and the data against furniture-design's rules.

The entries are kept in the private repo xag/furniture, checked out beside this one (or at $FURNITURE_REPO),
under sources/castorama/. Without them these tests fail, saying where they looked, and never skip.
"""

import hashlib
import json
import os
from pathlib import Path

from quern import Quern, run_rules

from furniture_design.knowledge import knowledge as general, merge
from furniture_design.package import PACKAGE
from wood_panels import knowledge as wood_panels
from wood_panels.shops import LINES, problems
from castorama_unofficial import knowledge, rows

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = Path(os.environ.get("FURNITURE_REPO", ROOT.parent / "furniture")) / "sources" / "castorama"


def _here(path: Path) -> Path:
    assert path.exists(), (f"the private copy {path} is missing: clone xag/furniture beside this repo or "
                           "set FURNITURE_REPO")
    return path


def test_every_product_is_its_sitemap_entry_and_reads_as_its_row():
    captured = json.loads(_here(CAPTURES / "sitemap-entries.json").read_text(encoding="utf-8"))
    assert problems(rows(), captured) == []
    assert captured["sitemaps"] and all(len(s) == 64 for s in captured["sitemaps"].values())


def test_every_line_the_range_names_is_described():
    assert {r["line"] for r in rows()} <= {line.id for line in LINES}


def test_no_two_materials_share_an_id():
    ids = [m.id for b in knowledge() if b.id == "materials" for m in b.children]
    assert len(ids) == len(set(ids))


def test_the_data_passes_furniture_designs_rules():
    tree = Quern(vocabulary=PACKAGE.vocabulary, rules=PACKAGE.rules, solvers=PACKAGE.solvers)
    tree.root.children = merge(general(), wood_panels(), knowledge())
    assert [(r.rule, r.node, r.verdict) for r in run_rules(tree) if not r.ok] == []


def test_the_cutting_service_refuses_what_its_page_does_not_list():
    tools = next(b for b in knowledge() if b.id == "tools").children
    (service,) = tools
    refused = set(service.links["refuses"])
    lines = {m.id: m.payload["shop"]["line"] for m in next(b for b in knowledge() if b.id == "materials").children}
    for m, line in lines.items():
        assert (f"materials/{m}" in refused) == (not line.startswith(('contreplaque', 'mdf', 'osb', 'agglomere', 'melamine'))), m
    assert {k: v for k, v in service.params.items()} == {}  # no cut, depth or narrowest part is published


def test_the_cutting_service_page_is_the_copy_kept():
    page = _here(CAPTURES / "services_decoupe.html")
    assert hashlib.sha256(page.read_bytes()).hexdigest() == "e0015051df502b76bf0030c95ca806425e025f1410b700e6878110f0e2b67687"
