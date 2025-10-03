"""Utility to inspect template layouts."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from agents.template_analyzer import TemplateAnalyzer


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a PPTX template and list layouts")
    parser.add_argument("template", type=Path, help="Path to template .pptx file")
    args = parser.parse_args()

    analyzer = TemplateAnalyzer(args.template)
    summary = analyzer.analyze()
    payload = [asdict(layout) for layout in summary.layouts]
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

