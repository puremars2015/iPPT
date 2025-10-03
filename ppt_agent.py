"""CLI entrypoint for the AI PPT Agent."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agents.content_generator import ContentGenerator
from agents.layout_matcher import LayoutMatcher
from agents.outline_manager import OutlineManager, OutlineParser
from agents.slide_generator import SlideGenerator
from agents.template_analyzer import TemplateAnalyzer
from config import settings
from core.logging import configure_logging, get_logger

logger = get_logger(__name__)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI PPT Agent CLI")
    parser.add_argument(
        "--template",
        required=True,
        type=Path,
        help="Path to the PowerPoint template (.pptx)",
    )
    parser.add_argument(
        "--title",
        type=str,
        help="Presentation document title metadata",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=0,
        help="Target number of slides (optional)",
    )
    parser.add_argument(
        "--outline",
        dest="outline_entries",
        action="append",
        required=True,
        help="Outline entries formatted as 'Title|bullet1,bullet2[,|image:path]'",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=settings.OUTPUT_DIR,
        help="Directory to store generated artefacts",
    )
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Disable placeholder image generation",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    template_path: Path = args.template
    if not template_path.exists():
        parser.error(f"Template not found: {template_path}")

    outline_items = OutlineParser.parse(args.outline_entries)
    if not outline_items:
        parser.error("No valid outline entries provided")

    target_pages = args.pages if args.pages > 0 else len(outline_items)

    logger.info("Starting AI PPT Agent")
    template_summary = TemplateAnalyzer(template_path).analyze()
    outline_summary = OutlineManager(target_pages=target_pages).organize(outline_items)
    plans = LayoutMatcher(template_summary).match(outline_summary)

    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    content_generator = ContentGenerator(output_dir=output_dir, enable_images=not args.skip_images)
    generated_slides = content_generator.generate(plans)

    slide_generator = SlideGenerator(
        template_path=template_path,
        template_summary=template_summary,
        output_dir=output_dir,
    )
    if args.title:
        slide_generator.presentation.core_properties.title = args.title

    output_path = slide_generator.build(plans, generated_slides)
    logger.info("Presentation ready: %s", output_path)

    print("Generated presentation:", output_path)
    if not args.skip_images and any(slide.image_path for slide in generated_slides):
        print("Generated images in:", content_generator.images_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())

