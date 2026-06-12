#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results.json"


def pct(value: float | None) -> str:
    return "-" if value is None else f"{value:.1f}%"


def score(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


def coverage(row: dict) -> str:
    return f"{row.get('ok', row.get('count', 0))}/{row.get('total', row.get('count', 0))}"


def table(title: str, headers: list[str], rows: list[list[str]]) -> str:
    out = [f"## {title}", "", "| " + " | ".join(headers) + " |"]
    out.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    out.append("")
    return "\n".join(out)


def main() -> None:
    data = json.loads(RESULTS.read_text(encoding="utf-8"))

    cross_rows = []
    for row in data["cross_language_prompt_by_model"]:
        cross_rows.append(
            [
                row["model"],
                coverage(row),
                pct(row["accuracy_percent"]),
                score(row["speaker_similarity_mean"]),
            ]
        )

    same_rows = []
    for row in data["same_language_prompt_by_model_language"]:
        same_rows.append(
            [
                row["model"],
                row["language_name"],
                coverage(row),
                pct(row["accuracy_percent"]),
                score(row["speaker_similarity_mean"]),
            ]
        )

    direction_rows = []
    for row in data["cross_language_prompt_by_direction"]:
        direction_rows.append(
            [
                row["model"],
                row["clone_direction"],
                coverage(row),
                pct(row["accuracy_percent"]),
                score(row["speaker_similarity_mean"]),
            ]
        )
    for row in data["unsupported_cross_language_directions"]:
        direction_rows.append(
            [
                row["model"],
                row["clone_direction"],
                coverage(row),
                pct(row["accuracy_percent"]),
                score(row["speaker_similarity_mean"]),
            ]
        )

    print(
        table(
            "Chinese/English Prompt -> Lao/Thai Target",
            ["Model", "Supported samples", "Accuracy", "Speaker similarity"],
            cross_rows,
        )
    )
    print(
        table(
            "Same-Language Prompt",
            ["Model", "Language", "Supported samples", "Accuracy", "Speaker similarity"],
            same_rows,
        )
    )
    print(
        table(
            "Direction-Level Cross-Language Prompt",
            ["Model", "Direction", "Supported samples", "Accuracy", "Speaker similarity"],
            direction_rows,
        )
    )


if __name__ == "__main__":
    main()
