#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results.json"
MODELS = ["Higgs Audio v3", "OmniVoice", "SE-Bridge-TTS", "X-Voice Stage1"]
LANGUAGE_NAMES = {"lo": "Lao", "th": "Thai", "zh": "Chinese", "en": "English"}
DIRECTION_ORDER = [
    ("lo", "lo", "lo_to_lo"),
    ("lo", "en", "en_to_lo"),
    ("lo", "zh", "zh_to_lo"),
    ("th", "th", "th_to_th"),
    ("th", "en", "en_to_th"),
    ("th", "zh", "zh_to_th"),
]


def pct(value: float | None) -> str:
    return "-" if value is None else f"{value:.1f}%"


def score(value: float | None, digits: int = 3) -> str:
    return "-" if value is None else f"{value:.{digits}f}"


def coverage(row: dict) -> str:
    return f"{row.get('ok', row.get('count', 0))}/{row.get('total', row.get('count', 0))}"


def rank_values(rows: list[dict], key: str, *, higher_is_better: bool) -> dict[str, int]:
    values = []
    for row in rows:
        value = row.get(key)
        if value is None:
            continue
        values.append((row["model"], float(value)))
    values.sort(key=lambda item: item[1], reverse=higher_is_better)

    ranks: dict[str, int] = {}
    rank = 0
    last_value = None
    for index, (model, value) in enumerate(values, 1):
        if last_value is None or value != last_value:
            rank = index
            last_value = value
        ranks[model] = rank
    return ranks


def mark(value: float | None, rank: int | None, *, percent: bool = False, digits: int = 3) -> str:
    text = pct(value) if percent else score(value, digits)
    if rank == 1:
        return f"**{text}**"
    if rank == 2:
        return f"<u>{text}</u>"
    return text


def table(title: str, headers: list[str], rows: list[list[str]]) -> str:
    out = [f"## {title}", "", "| " + " | ".join(headers) + " |"]
    out.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    out.append("")
    return "\n".join(out)


def aggregate_table(data: dict) -> str:
    rows = data["cross_language_prompt_by_model"]
    acc_ranks = rank_values(rows, "accuracy_percent", higher_is_better=True)
    sim_ranks = rank_values(rows, "speaker_similarity_mean", higher_is_better=True)

    rendered = []
    for model in MODELS:
        row = next(item for item in rows if item["model"] == model)
        rendered.append(
            [
                model,
                coverage(row),
                mark(row["accuracy_percent"], acc_ranks.get(model), percent=True),
                mark(row["speaker_similarity_mean"], sim_ranks.get(model)),
            ]
        )
    return table(
        "Chinese/English Prompt -> Lao/Thai Target",
        ["Model", "Supported samples", "Accuracy", "Speaker similarity"],
        rendered,
    )


def direction_rows(data: dict) -> list[dict]:
    rows = []
    for row in data["same_language_prompt_by_model_language"]:
        rows.append(
            {
                **row,
                "clone_direction": f"{row['language_id']}_to_{row['language_id']}",
                "prompt_language_id": row["language_id"],
                "target_language_id": row["language_id"],
                "prompt_language_name": row["language_name"],
                "target_language_name": row["language_name"],
            }
        )
    rows.extend(data["cross_language_prompt_by_direction"])
    rows.extend(data["unsupported_cross_language_directions"])
    return rows


def direction_table(data: dict) -> str:
    by_direction: dict[str, list[dict]] = defaultdict(list)
    for row in direction_rows(data):
        by_direction[row["clone_direction"]].append(row)

    rendered = []
    for target_id, prompt_id, direction in DIRECTION_ORDER:
        rows = by_direction[direction]
        cer_ranks = rank_values(rows, "calibrated_cer_mean", higher_is_better=False)
        sim_ranks = rank_values(rows, "speaker_similarity_mean", higher_is_better=True)
        by_model = {row["model"]: row for row in rows}

        cells = []
        for model in MODELS:
            row = by_model.get(model)
            if row is None:
                cells.append("-")
                continue
            cer = mark(row.get("calibrated_cer_mean"), cer_ranks.get(model), digits=4)
            sim = mark(row.get("speaker_similarity_mean"), sim_ranks.get(model))
            cells.append(f"{cer} / {sim}")

        rendered.append(
            [
                LANGUAGE_NAMES[target_id],
                LANGUAGE_NAMES[prompt_id],
                *cells,
            ]
        )

    return table(
        "Prompt-Language Voice Cloning Details",
        [
            "Target",
            "Prompt",
            "Higgs Audio v3",
            "OmniVoice",
            "SE-Bridge-TTS",
            "X-Voice Stage1",
        ],
        rendered,
    )


def main() -> None:
    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    print(aggregate_table(data))
    print("Each detail cell is `Cal. CER↓ / SIM↑`. Best is **bold**; second best is <u>underlined</u>.")
    print()
    print(direction_table(data))


if __name__ == "__main__":
    main()
