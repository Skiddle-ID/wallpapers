"""Classification for AI detection and Wallpaper Categorization."""

import re
from pathlib import Path
from typing import Dict, NamedTuple, Optional, Tuple
from PIL import Image

from .config import CATEGORIES, TYPES


class ClassificationResult(NamedTuple):
    type: str  # "AI", "NON-AI", "UNKNOWN"
    category: str  # One of the 15 official categories
    ai_confidence: float  # 0.0 to 1.0


# Keyword patterns for category assignment
CATEGORY_PATTERNS = {
    "Cyberpunk": [
        r"\bcyberpunk\b", r"\bneon\b", r"\bfuturistic\b", r"\bsynthwave\b",
        r"\bretro wave\b", r"\bblade[-_ ]runner\b", r"\bcyber\b", r"\bmecha\b"
    ],
    "Sci-Fi": [
        r"\bsci[-_ ]?fi\b", r"\bscience[-_ ]fiction\b", r"\bspaceship\b",
        r"\brobot\b", r"\balien\b", r"\bcyborg\b", r"\bfuture\b", r"\bportal\b"
    ],
    "Space": [
        r"\bspace\b", r"\bgalaxy\b", r"\bnebula\b", r"\bplanet\b",
        r"\bastronomy\b", r"\bcosmos\b", r"\bstar\b", r"\bstars\b", r"\bsolar\b", r"\bmoon\b"
    ],
    "Anime": [
        r"\banime\b", r"\bmanga\b", r"\bwaifu\b", r"\bgirl\b", r"\bboy\b",
        r"\bchibi\b", r"\bpikachu\b", r"\bpokemon\b", r"\bpokémon\b", r"\bcharizard\b",
        r"\bbulbasaur\b", r"\bcharmander\b", r"\beevee\b", r"\bgengar\b", r"\bgenshin\b",
        r"\bhonkai\b", r"\bcartoon\b", r"\bcomic\b"
    ],
    "Gaming": [
        r"\bgames?\b", r"\bgaming\b", r"\bgamer\b", r"\bendfield\b",
        r"\bwuwa\b", r"\bwuthering\b", r"\barknights\b", r"\bzelda\b",
        r"\bmario\b", r"\bplaystation\b", r"\bxbox\b", r"\bnintendo\b",
        r"\bsteam\b", r"\besports\b", r"\bvalorant\b", r"\bminecraft\b"
    ],
    "Cars": [
        r"\bcars?\b", r"\bauto\b", r"\bautomobile\b", r"\bvehicle\b",
        r"\bsupercar\b", r"\bferrari\b", r"\blamborghini\b", r"\bporsche\b",
        r"\bmclaren\b", r"\bmotorcycle\b", r"\bdrift\b", r"\bracing\b"
    ],
    "City": [
        r"\bcity\b", r"\bstreet\b", r"\btokyo\b", r"\burban\b",
        r"\bskyline\b", r"\btown\b", r"\bdowntown\b", r"\bmetropolis\b",
        r"\broad\b", r"\balley\b", r"\bbuilding\b", r"\bclock[-_ ]tower\b"
    ],
    "Architecture": [
        r"\barchitecture\b", r"\bcathedral\b", r"\bbridge\b",
        r"\btemple\b", r"\bmonument\b", r"\bpalace\b", r"\bstructure\b", r"\bhouse\b"
    ],
    "Ocean": [
        r"\bocean\b", r"\bsea\b", r"\bbeach\b", r"\bunderwater\b",
        r"\bmarine\b", r"\bcoral\b", r"\bwave\b", r"\bcoast\b", r"\bcoastal\b"
    ],
    "Nature": [
        r"\bnature\b", r"\bforest\b", r"\btrees?\b", r"\bplants?\b",
        r"\bflowers?\b", r"\bjungle\b", r"\bgarden\b", r"\bbamboo\b",
        r"\bbird\b", r"\banimal\b", r"\bwildlife\b", r"\bwaterfall\b"
    ],
    "Landscape": [
        r"\blandscape\b", r"\bmountain\b", r"\bmountains\b", r"\blake\b",
        r"\briver\b", r"\bhills?\b", r"\bvalley\b", r"\bsunset\b",
        r"\bsunrise\b", r"\bfield\b", r"\bhorizon\b", r"\bview\b", r"\bcliff\b"
    ],
    "Fantasy": [
        r"\bfantasy\b", r"\bmagic\b", r"\bmagical\b", r"\bdragon\b",
        r"\bcastle\b", r"\bfloating[-_ ]island\b", r"\belf\b", r"\bfairy\b",
        r"\bmythical\b", r"\bcreature\b"
    ],
    "People": [
        r"\bpeople\b", r"\bperson\b", r"\bportrait\b", r"\bman\b",
        r"\bwoman\b", r"\bmodel\b", r"\bface\b", r"\bhuman\b"
    ],
    "Abstract": [
        r"\babstract\b", r"\bminimal\b", r"\bminimalist\b", r"\bgradient\b",
        r"\bgeometric\b", r"\b3d[-_ ]render\b", r"\btexture\b", r"\bpattern\b",
        r"\bpoly\b", r"\bfluid\b"
    ],
}


def normalize_text(text: str) -> str:
    """Normalize text by replacing separators and non-alphanumeric chars with spaces."""
    return re.sub(r"[^a-zA-Z0-9]+", " ", text).lower()


def extract_metadata_strings(file_path: Path) -> str:
    """Extract string metadata from image EXIF and PNG text info."""
    meta_strings = []
    try:
        with Image.open(file_path) as img:
            if hasattr(img, "info") and img.info:
                for k, v in img.info.items():
                    if isinstance(v, str):
                        meta_strings.append(f"{k}: {v}")
            exif = img.getexif()
            if exif:
                for tag_id, val in exif.items():
                    if isinstance(val, str):
                        meta_strings.append(str(val))
    except Exception:
        pass
    return " ".join(meta_strings)


def classify_ai(
    file_path: Path,
    source: Optional[str] = None,
    source_url: Optional[str] = None,
    metadata_hint: Optional[Dict] = None,
) -> Tuple[str, float]:
    """
    Classify whether image is AI, NON-AI, or UNKNOWN.
    Returns (classification, confidence).
    """
    hint_type = (metadata_hint or {}).get("type")
    if hint_type in TYPES:
        return hint_type, 1.0

    raw_text = f"{file_path.name} {file_path.parent.name} {source or ''} {source_url or ''}"
    meta_str = extract_metadata_strings(file_path)
    combined = normalize_text(f"{raw_text} {meta_str}")

    # Check for strong AI indicators
    ai_patterns = [
        r"\bskiddle\s+generated\b",
        r"\bmidjourney\b",
        r"\bstable\s+diffusion\b",
        r"\bdall\s*e\b",
        r"\bnovelai\b",
        r"\bcomfyui\b",
        r"\bautomatic1111\b",
        r"\blexica\b",
        r"\bcivitai\b",
        r"\bai\s+generated\b",
        r"\bai\s+art\b",
    ]

    for pat in ai_patterns:
        if re.search(pat, combined):
            return "AI", 0.95

    # Check for strong Non-AI indicators (photographs with camera EXIF, official studios)
    non_ai_patterns = [
        r"\bnikon\b", r"\bcanon\b", r"\bsony\b", r"\bfujifilm\b",
        r"\bunsplash\b", r"\bpixabay\b", r"\buhdpaper\b",
        r"\bpokemon\b", r"\bpikachu\b", r"\bnintendo\b",
        r"\bendfield\b", r"\bwuwa\b", r"\barknights\b"
    ]

    for pat in non_ai_patterns:
        if re.search(pat, combined):
            return "NON-AI", 0.85

    # Default to UNKNOWN when origin cannot be determined with confidence
    return "UNKNOWN", 0.5


def classify_category(
    file_path: Path,
    category_hint: Optional[str] = None,
    source_url: Optional[str] = None
) -> str:
    """
    Assign one of the 15 official categories.
    """
    # If a valid category hint is provided, validate and use it
    if category_hint:
        normalized_hint = category_hint.strip()
        # Map common legacy synonyms
        synonyms = {
            "Anime": "Anime",
            "Pokémon": "Anime",
            "Pokemon": "Anime",
            "Games": "Gaming",
            "Gaming": "Gaming",
            "Nature": "Nature",
            "Calm": "Landscape",
            "City": "City",
            "Cars": "Cars",
            "Cyberpunk": "Cyberpunk",
            "Fantasy": "Fantasy",
            "Landscape": "Landscape",
            "Ocean": "Ocean",
            "People": "People",
            "Sci-Fi": "Sci-Fi",
            "Space": "Space",
            "Abstract": "Abstract",
            "Architecture": "Architecture",
        }
        if normalized_hint in CATEGORIES:
            return normalized_hint
        if normalized_hint in synonyms:
            return synonyms[normalized_hint]

    # Analyze file name, directory, and source url
    raw_text = f"{file_path.name} {file_path.parent.name} {source_url or ''}"
    text = normalize_text(raw_text)

    # Score categories based on regex matches
    scores: Dict[str, int] = {cat: 0 for cat in CATEGORIES}

    for cat, patterns in CATEGORY_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text):
                scores[cat] += 1

    best_cat, best_score = max(scores.items(), key=lambda item: item[1])

    if best_score > 0:
        return best_cat

    # Fallback to Other
    return "Other"


def classify_image(
    file_path: Path,
    source: Optional[str] = None,
    source_url: Optional[str] = None,
    category_hint: Optional[str] = None,
    metadata_hint: Optional[Dict] = None,
) -> ClassificationResult:
    """
    Perform full classification on an image file.
    """
    ai_type, confidence = classify_ai(
        file_path,
        source=source,
        source_url=source_url,
        metadata_hint=metadata_hint
    )
    category = classify_category(
        file_path,
        category_hint=category_hint,
        source_url=source_url
    )
    return ClassificationResult(
        type=ai_type,
        category=category,
        ai_confidence=confidence
    )
