"""Layout selection heuristics."""
from __future__ import annotations

from typing import List

from config import settings
from core.logging import get_logger
from core.models import OutlineSummary, SlidePlan, TemplateLayout, TemplateSummary

logger = get_logger(__name__)


class LayoutMatcher:
    def __init__(self, template_summary: TemplateSummary) -> None:
        self.template_summary = template_summary
        self.layouts = template_summary.layouts

    def match(self, outline: OutlineSummary) -> List[SlidePlan]:
        plans: List[SlidePlan] = []
        for idx, item in enumerate(outline.items):
            layout = self._select_layout(idx)
            plans.append(SlidePlan(layout=layout, outline=item))
        logger.info("Matched %d slides to layouts", len(plans))
        return plans

    def _select_layout(self, slide_index: int) -> TemplateLayout:
        if slide_index == 0:
            layout = self._find_by_kind("title")
            if layout:
                return layout
        layout = self._find_by_kind("content")
        if layout:
            return layout
        layout = self._find_by_kind("content_two")
        if layout:
            return layout
        fallback = self._find_by_name(settings.FALLBACK_LAYOUT_KEY)
        if fallback:
            return fallback
        logger.warning("Falling back to first available layout")
        return self.layouts[0]

    def _find_by_kind(self, kind: str) -> TemplateLayout | None:
        for layout in self.layouts:
            if layout.kind == kind:
                return layout
        return None

    def _find_by_name(self, name: str) -> TemplateLayout | None:
        name = name.lower()
        for layout in self.layouts:
            if layout.name.lower() == name:
                return layout
        return None

