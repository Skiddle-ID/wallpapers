"""Configuration constants for the Wallpaper Collection Agent."""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
WALLPAPERS_DIR = BASE_DIR / "Wallpapers"
INCOMING_DIR = BASE_DIR / "incoming"
DB_PATH = BASE_DIR / "wallpapers.db"

# Minimum Resolution: 2K or higher (2560 x 1440 = 3,686,400 pixels)
MIN_PIXELS = 2560 * 1440  # 3,686,400

# Classification Types
TYPES = ["AI", "NON-AI", "UNKNOWN"]

# 15 Primary Categories
CATEGORIES = [
    "Anime",
    "Architecture",
    "Abstract",
    "Cars",
    "City",
    "Cyberpunk",
    "Fantasy",
    "Gaming",
    "Landscape",
    "Nature",
    "Ocean",
    "People",
    "Sci-Fi",
    "Space",
    "Other",
]

# Perceptual hash hamming distance threshold for visual duplicates
# Distance 0: Exact visual match
# Distance <= 5: Very high visual similarity
PHASH_SIMILARITY_THRESHOLD = 5

# Supported file extensions
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
