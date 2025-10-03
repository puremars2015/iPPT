"""Application-wide settings for the AI PPT agent CLI."""
from pathlib import Path

# Default output artefacts
OUTPUT_DIR = Path("output")
PRESENTATION_NAME = "output.pptx"
IMAGES_DIR_NAME = "images"
# Layout heuristics
COMMON_LAYOUT_ALIASES = {
    "title slide": "title",
    "title slide " : "title",  # fallback due to trailing spaces in some templates
    "title": "title",
    "title and content": "content",
    "title+content": "content",
    "two content": "content_two",
    "two column": "content_two",
}
FALLBACK_LAYOUT_KEY = "title and content"

# Generation defaults
MAX_BULLETS_PER_SLIDE = 10
SENTENCE_ENDINGS = ("。", ".", "!", "！", "?", "？")
SUMMARY_SUFFIX = "："

# Image generation
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 360
BACKGROUND_COLOR = (245, 248, 252)
TEXT_COLOR = (33, 37, 41)
FONT_FALLBACK = "DejaVuSans-Bold.ttf"

