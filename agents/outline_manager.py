"""Outline processing and pagination logic."""
from __future__ import annotations

from typing import Iterable, List, Tuple

from config import settings
from core.logging import get_logger
from core.models import OutlineItem, OutlineSummary

logger = get_logger(__name__)


class OutlineParser:
    @staticmethod
    def parse(raw_entries: Iterable[str]) -> List[OutlineItem]:
        items: List[OutlineItem] = []
        for raw in raw_entries:
            raw = raw.strip()
            raw = raw.strip("\"")
            raw = raw.strip("'")  # tolerate quoting artifacts
            if not raw:
                continue
            parts = [part.strip() for part in raw.split("|") if part.strip()]
            if not parts:
                continue
            title = parts[0]
            bullets: List[str] = []
            image_hint = None
            for section in parts[1:]:
                if section.lower().startswith("image:"):
                    image_hint = section.split(":", 1)[1].strip() or None
                else:
                    bullets.extend([b.strip() for b in section.split(",") if b.strip()])
            if not bullets:
                bullets = ["請填寫內容"]
            items.append(OutlineItem(title=title, bullets=bullets, image_hint=image_hint))
        return items


class OutlineManager:
    def __init__(self, target_pages: int) -> None:
        self.target_pages = target_pages

    def organize(self, items: List[OutlineItem]) -> OutlineSummary:
        logger.info("Organizing outline into %d pages", self.target_pages)
        normalized = self._split_long_bullets(items)
        adjusted = self._meet_page_target(normalized)
        return OutlineSummary(items=adjusted)

    def _split_long_bullets(self, items: List[OutlineItem]) -> List[OutlineItem]:
        result: List[OutlineItem] = []
        for item in items:
            bullets = item.bullets
            if len(bullets) <= settings.MAX_BULLETS_PER_SLIDE:
                result.append(item)
                continue
            chunks = [
                bullets[i : i + settings.MAX_BULLETS_PER_SLIDE]
                for i in range(0, len(bullets), settings.MAX_BULLETS_PER_SLIDE)
            ]
            total = len(chunks)
            for index, chunk in enumerate(chunks, start=1):
                suffix = f" (Part {index}/{total})"
                result.append(
                    OutlineItem(
                        title=f"{item.title}{suffix}",
                        bullets=chunk,
                        image_hint=item.image_hint,
                    )
                )
        return result

    def _meet_page_target(self, items: List[OutlineItem]) -> List[OutlineItem]:
        if self.target_pages <= 0:
            return items
        items = list(items)
        while len(items) > self.target_pages and len(items) > 1:
            merge_index = self._find_merge_index(items)
            first = items.pop(merge_index)
            second = items.pop(merge_index)
            merged_title = f"{first.title} / {second.title}"
            merged_bullets = first.bullets + second.bullets
            merged_hint = first.image_hint or second.image_hint
            items.insert(
                merge_index,
                OutlineItem(title=merged_title, bullets=merged_bullets, image_hint=merged_hint),
            )
        split_round = 1
        while len(items) < self.target_pages and items:
            idx = self._find_split_index(items)
            outline = items.pop(idx)
            first, second = self._split_outline(outline)
            items.insert(idx, second)
            items.insert(idx, first)
            split_round += 1
            if split_round > self.target_pages * 2:
                logger.warning("Unable to reach target pages cleanly; returning current items")
                break
        return items

    def _find_merge_index(self, items: List[OutlineItem]) -> int:
        min_total = float("inf")
        min_index = 0
        for idx in range(len(items) - 1):
            total = len(items[idx].bullets) + len(items[idx + 1].bullets)
            if total < min_total:
                min_total = total
                min_index = idx
        return min_index

    def _find_split_index(self, items: List[OutlineItem]) -> int:
        max_bullets = max(len(item.bullets) for item in items)
        for idx, item in enumerate(items):
            if len(item.bullets) == max_bullets:
                return idx
        return 0

    def _split_outline(self, item: OutlineItem) -> Tuple[OutlineItem, OutlineItem]:
        if len(item.bullets) <= 1:
            first = OutlineItem(title=f"{item.title} (Part 1)", bullets=item.bullets, image_hint=item.image_hint)
            second = OutlineItem(
                title=f"{item.title} (Part 2)",
                bullets=[f"延伸：{item.bullets[0]}"] if item.bullets else ["延伸討論"],
                image_hint=item.image_hint,
            )
            return first, second
        mid = len(item.bullets) // 2
        first_bullets = item.bullets[:mid]
        second_bullets = item.bullets[mid:]
        return (
            OutlineItem(title=f"{item.title} (Part 1)", bullets=first_bullets, image_hint=item.image_hint),
            OutlineItem(title=f"{item.title} (Part 2)", bullets=second_bullets, image_hint=item.image_hint),
        )

