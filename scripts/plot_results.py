"""Generate benchmark PNG charts from the latest report."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATHS = [ROOT / "results" / "report_v2.json", ROOT / "results" / "report.json"]
FIGURES_DIR = ROOT / "docs" / "figures"

METRICS = [
    ("policy_violation_rate", "Policy Violation Rate", "rate"),
    ("token_overspend_rate", "Token Overspend Rate", "rate"),
    ("persona_drift_rate", "Persona Drift Rate", "rate"),
    ("audit_reconstruction_time", "Audit Reconstruction Time", "seconds"),
    ("decision_latency", "Decision Latency", "seconds"),
]


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def _format_value(value: float, unit: str) -> str:
    if unit == "rate":
        return f"{value * 100:.1f}%"
    return f"{value:.4f}s" if value < 1 else f"{value:.2f}s"


def _load_report() -> dict:
    for path in REPORT_PATHS:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    raise FileNotFoundError("No benchmark report found. Run the scenario scripts first.")


def _draw_chart(metric_key: str, title: str, unit: str, baseline: float, governed: float, output_path: Path) -> None:
    width, height = 1100, 720
    image = Image.new("RGB", (width, height), "#f7f5ef")
    draw = ImageDraw.Draw(image)

    title_font = _load_font(40)
    label_font = _load_font(28)
    value_font = _load_font(26)
    small_font = _load_font(22)

    draw.rectangle((0, 0, width, height), fill="#f7f5ef")
    draw.text((70, 40), title, fill="#1d2935", font=title_font)
    draw.text((70, 95), "Baseline vs Governed", fill="#5f6e7a", font=small_font)

    left, right = 120, width - 120
    top, bottom = 180, height - 140
    chart_width = right - left
    chart_height = bottom - top

    draw.line((left, top, left, bottom), fill="#8e9aa4", width=3)
    draw.line((left, bottom, right, bottom), fill="#8e9aa4", width=3)

    max_value = max(baseline, governed, 1.0 if unit == "rate" else 0.1)
    if unit == "rate":
        max_value = max(1.0, max_value)
    else:
        max_value = max_value * 1.15

    for step in range(6):
        y = bottom - chart_height * step / 5
        draw.line((left - 10, y, right, y), fill="#e1ddd2", width=1)
        tick_value = max_value * step / 5
        draw.text((30, y - 12), _format_value(tick_value, unit), fill="#5f6e7a", font=small_font)

    bars = [
        ("Baseline", baseline, "#b56d4f"),
        ("Governed", governed, "#3f7d6b"),
    ]
    bar_width = 180
    gap = 150
    first_x = left + (chart_width - (2 * bar_width + gap)) // 2

    for index, (label, value, color) in enumerate(bars):
        x0 = first_x + index * (bar_width + gap)
        x1 = x0 + bar_width
        bar_height = 0 if max_value == 0 else chart_height * (value / max_value)
        y0 = bottom - bar_height
        draw.rounded_rectangle((x0, y0, x1, bottom), radius=18, fill=color)
        bbox = draw.textbbox((0, 0), label, font=label_font)
        label_width = bbox[2] - bbox[0]
        draw.text((x0 + (bar_width - label_width) / 2, bottom + 18), label, fill="#1d2935", font=label_font)
        value_text = _format_value(value, unit)
        value_bbox = draw.textbbox((0, 0), value_text, font=value_font)
        value_width = value_bbox[2] - value_bbox[0]
        draw.text((x0 + (bar_width - value_width) / 2, y0 - 38), value_text, fill="#1d2935", font=value_font)

    draw.text((70, height - 70), f"Metric key: {metric_key}", fill="#5f6e7a", font=small_font)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def main() -> None:
    report = _load_report()
    summary = report["summary"]
    baseline = summary["baseline"]
    governed = summary["governed"]

    for metric_key, title, unit in METRICS:
        _draw_chart(
            metric_key,
            title,
            unit,
            float(baseline[metric_key]),
            float(governed[metric_key]),
            FIGURES_DIR / f"{metric_key}.png",
        )


if __name__ == "__main__":
    main()
