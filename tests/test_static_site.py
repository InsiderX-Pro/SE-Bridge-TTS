import json
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag in {"link", "script"}:
            self.links.append(attrs.get("href") or attrs.get("src"))


def test_required_pages_assets_and_data_exist():
    expected_files = [
        "index.html",
        "README.md",
        "assets/data/demo-data.json",
        "assets/figures/dgsa.png",
        "assets/figures/tdsc.png",
        "paper/MultiLanTTS_camera_v0.1.pdf",
    ]

    missing = [path for path in expected_files if not (ROOT / path).exists()]

    assert missing == []


def test_demo_data_references_existing_assets():
    data = json.loads((ROOT / "assets/data/demo-data.json").read_text(encoding="utf-8"))

    assert data["paper"]["title"].startswith("Bridging the Stability-Expressivity Gap")
    assert data["paper"]["venue"] == "ICML 2026"
    assert {section["id"] for section in data["sections"]} == {
        "benchmarks",
        "cloning",
        "erosion",
        "dgsa",
        "tdsc",
    }

    missing = []
    for figure in data["figures"]:
        if not (ROOT / figure["src"]).exists():
            missing.append(figure["src"])
    for section in data["sections"]:
        for group in section["groups"]:
            for sample in group["samples"]:
                for audio in sample["audios"]:
                    if not (ROOT / audio["src"]).exists():
                        missing.append(audio["src"])

    assert missing == []


def test_index_contains_academic_project_sections():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    parser = IdCollector()
    parser.feed(html)

    for section_id in [
        "overview",
        "key-idea",
        "methods",
        "audio-demo",
        "results",
        "citation",
    ]:
        assert section_id in parser.ids

    assert "assets/data/demo-data.json" in html
    assert "Code coming soon" in html
