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

# Expanded Primary Categories (25 categories)
CATEGORIES = [
    "Abstract",
    "Animals",
    "Anime",
    "Architecture",
    "Cars",
    "City",
    "Comics",
    "Cyberpunk",
    "Digital Art",
    "Fantasy",
    "Gaming",
    "Horror",
    "Landscape",
    "Military",
    "Minimalism",
    "Music",
    "Nature",
    "Ocean",
    "People",
    "Pixel Art",
    "Sci-Fi",
    "Space",
    "Sports",
    "Vehicles",
    "Other",
]

# Perceptual hash hamming distance threshold for visual duplicates
PHASH_SIMILARITY_THRESHOLD = 5

# Supported file extensions
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
