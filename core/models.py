"""Domain models shared across agent components."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class TemplateLayout:
    index: int
    name: str
    kind: str
    placeholders: Dict[str, int]
    is_common: bool


@dataclass
class TemplateSummary:
    layouts: List[TemplateLayout]


@dataclass
class OutlineItem:
    title: str
    bullets: List[str]
    image_hint: Optional[str] = None


@dataclass
class OutlineSummary:
    items: List[OutlineItem]


@dataclass
class SlidePlan:
    layout: TemplateLayout
    outline: OutlineItem


@dataclass
class GeneratedSlide:
    title: str
    bullet_sentences: List[str]
    outline: OutlineItem
    image_path: Optional[Path] = None
    notes: Dict[str, str] = field(default_factory=dict)

