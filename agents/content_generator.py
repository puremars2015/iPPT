"""Content expansion and asset generation."""
from __future__ import annotations

import textwrap
from pathlib import Path
from typing import List, Optional

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - optional dependency
    Image = None  # type: ignore

from config import settings
from core.logging import get_logger
from core.models import GeneratedSlide, OutlineItem, SlidePlan

logger = get_logger(__name__)


class ContentGenerator:
    def __init__(self, output_dir: Path, enable_images: bool = True) -> None:
        self.output_dir = output_dir
        self.enable_images = enable_images
        self.images_dir = self.output_dir / settings.IMAGES_DIR_NAME
        if self.enable_images:
            self.images_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, plans: List[SlidePlan]) -> List[GeneratedSlide]:
        slides: List[GeneratedSlide] = []
        for index, plan in enumerate(plans, start=1):
            sentences = [self._expand_bullet(bullet) for bullet in plan.outline.bullets]
            image_path = self._maybe_generate_image(index, plan.outline)
            slides.append(
                GeneratedSlide(
                    title=plan.outline.title,
                    bullet_sentences=sentences,
                    outline=plan.outline,
                    image_path=image_path,
                )
            )
        return slides

    def _expand_bullet(self, bullet: str) -> str:
        clean = bullet.strip()
        if not clean:
            return "待補充內容。"
        if clean.endswith(settings.SENTENCE_ENDINGS):
            return clean
        if "：" in clean or ":" in clean:
            return clean.rstrip("。") + "。"
        return f"{clean}：聚焦此主題的關鍵重點。"

    def _maybe_generate_image(self, index: int, outline: OutlineItem) -> Optional[Path]:
        if not self.enable_images:
            return None
        hint = outline.image_hint or (outline.bullets[0] if outline.bullets else outline.title)
        if not hint:
            return None
        if Image is None:
            logger.debug("Pillow not installed; skipping image generation")
            return None
        output_path = self.images_dir / f"slide_{index:02d}.png"
        create_placeholder_image(
            text=hint,
            output_path=output_path,
            title=outline.title,
        )
        return output_path


def create_placeholder_image(text: str, output_path: Path, title: str) -> None:
    image = Image.new("RGB", (settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT), color=settings.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(settings.FONT_FALLBACK, 28)
        subtitle_font = ImageFont.truetype(settings.FONT_FALLBACK, 20)
    except OSError:
        font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    wrapped_title = textwrap.fill(title, width=18)
    wrapped_text = textwrap.fill(text, width=24)
    draw.text((40, 40), wrapped_title, fill=settings.TEXT_COLOR, font=font)
    draw.text((40, 120), wrapped_text, fill=settings.TEXT_COLOR, font=subtitle_font)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    logger.debug("Generated placeholder image at %s", output_path)

