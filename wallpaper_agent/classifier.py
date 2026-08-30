"""Classification for AI detection and Wallpaper Categorization."""

import re
from pathlib import Path
from typing import Any, Dict, NamedTuple, Optional, Tuple
from PIL import Image
from PIL.ExifTags import TAGS

from .config import CATEGORIES, TYPES
from .vision_classifier import classify_image_visually, is_vision_available


class ClassificationResult(NamedTuple):
    type: str  # "AI", "NON-AI", "UNKNOWN"
    category: str  # One of the official categories
    ai_confidence: float  # 0.0 to 1.0
    detected_signals: str = ""  # Explanation of detected signals


# Keyword patterns for category assignment
CATEGORY_PATTERNS = {
    "Cyberpunk": [
        r"\bcyberpunk\b", r"\bneon\b", r"\bfuturistic\b", r"\bsynthwave\b",
        r"\bretro\s*wave\b", r"\bblade\s*runner\b", r"\bcyber\b", r"\bmecha\b"
    ],
    "Sci-Fi": [
        r"\bsci\s*fi\b", r"\bscience\s*fiction\b", r"\bspaceship\b",
        r"\brobot\b", r"\balien\b", r"\bcyborg\b", r"\bfuture\b", r"\bportal\b"
    ],
    "Space": [
        r"\bspace\b", r"\bgalaxy\b", r"\bnebula\b", r"\bplanet\b",
        r"\bastronomy\b", r"\bcosmos\b", r"\bstar\b", r"\bstars\b", r"\bsolar\b", r"\bmoon\b"
    ],
    "Anime": [
        r"\banime\b", r"\bmanga\b", r"\bwaifu\b", r"\bgirl\b", r"\bboy\b",
        r"\bchibi\b", r"\bpikachu\b", r"\bpokemon\b", r"\bcharizard\b",
        r"\bbulbasaur\b", r"\bcharmander\b", r"\beevee\b", r"\bgengar\b", r"\bgenshin\b",
        r"\bhonkai\b", r"\bcartoon\b"
    ],
    "Gaming": [
        r"\bgames?\b", r"\bgaming\b", r"\bgamer\b", r"\bendfield\b",
        r"\bwuwa\b", r"\bwuthering\b", r"\barknights\b", r"\bzelda\b",
        r"\bmario\b", r"\bplaystation\b", r"\bxbox\b", r"\bnintendo\b",
        r"\bsteam\b", r"\besports\b", r"\bvalorant\b", r"\bminecraft\b"
    ],
    "Cars": [
        r"\bcars?\b", r"\bauto\b", r"\bautomobile\b",
        r"\bsupercar\b", r"\bferrari\b", r"\blamborghini\b", r"\bporsche\b",
        r"\bmclaren\b", r"\bdrift\b", r"\bracing\b"
    ],
    "Vehicles": [
        r"\bmotorcycle\b", r"\bmotorbike\b", r"\baviation\b", r"\bhelicopter\b",
        r"\btrain\b", r"\byacht\b", r"\bplane\b", r"\bairplane\b", r"\bvehicle\b"
    ],
    "Military": [
        r"\bmilitary\b", r"\barmy\b", r"\bnavy\b", r"\btank\b",
        r"\bfighter\s*jet\b", r"\bwarplane\b", r"\bsoldier\b", r"\bweapon\b"
    ],
    "Comics": [
        r"\bcomics?\b", r"\bmarvel\b", r"\bdc\b", r"\bsuperhero\b",
        r"\bbatman\b", r"\bspiderman\b", r"\bsuperman\b", r"\bavengers\b", r"\bjoker\b"
    ],
    "Pixel Art": [
        r"\bpixel\s*art\b", r"\b8\s*bit\b", r"\b16\s*bit\b",
        r"\bretro\s*game\b", r"\bvoxel\b", r"\bbitart\b"
    ],
    "Animals": [
        r"\banimals?\b", r"\bwildlife\b", r"\bcat\b", r"\bdog\b",
        r"\blion\b", r"\btiger\b", r"\bwolf\b", r"\bbird\b", r"\beagle\b",
        r"\bfox\b", r"\bbear\b", r"\bdeer\b", r"\bhorse\b"
    ],
    "City": [
        r"\bcity\b", r"\bstreet\b", r"\btokyo\b", r"\burban\b",
        r"\bskyline\b", r"\btown\b", r"\bdowntown\b", r"\bmetropolis\b",
        r"\broad\b", r"\balley\b", r"\bbuilding\b", r"\bclock\s*tower\b"
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
        r"\bflowers?\b", r"\bjungle\b", r"\bgarden\b", r"\bbamboo\b", r"\bwaterfall\b"
    ],
    "Landscape": [
        r"\blandscape\b", r"\bmountain\b", r"\bmountains\b", r"\blake\b",
        r"\briver\b", r"\bhills?\b", r"\bvalley\b", r"\bsunset\b",
        r"\bsunrise\b", r"\bfield\b", r"\bhorizon\b", r"\bview\b", r"\bcliff\b"
    ],
    "Fantasy": [
        r"\bfantasy\b", r"\bmagic\b", r"\bmagical\b", r"\bdragon\b",
        r"\bcastle\b", r"\bfloating\s*island\b", r"\belf\b", r"\bfairy\b",
        r"\bmythical\b", r"\bcreature\b"
    ],
    "Horror": [
        r"\bhorror\b", r"\bskull\b", r"\bskeleton\b", r"\bmonster\b",
        r"\bdark\s*fantasy\b", r"\bgothic\b", r"\bzombie\b", r"\bspooky\b"
    ],
    "Music": [
        r"\bmusic\b", r"\bguitar\b", r"\bpiano\b", r"\bdrums\b",
        r"\binstruments?\b", r"\bconcert\b", r"\bheadphones\b", r"\bdj\b"
    ],
    "Sports": [
        r"\bsports?\b", r"\bbasketball\b", r"\bfootball\b", r"\bsoccer\b",
        r"\bskateboard\b", r"\bsurfing\b", r"\bfitness\b"
    ],
    "Digital Art": [
        r"\bdigital\s*art\b", r"\bconcept\s*art\b", r"\b3d\s*render\b",
        r"\bartstation\b", r"\billustration\b", r"\bcgi\b"
    ],
    "Minimalism": [
        r"\bminimal\b", r"\bminimalist\b", r"\bminimalism\b",
        r"\bflat\s*art\b", r"\bvector\b", r"\bamoled\b", r"\boled\b", r"\bmonochrome\b"
    ],
    "People": [
        r"\bpeople\b", r"\bperson\b", r"\bportrait\b", r"\bman\b",
        r"\bwoman\b", r"\bmodel\b", r"\bface\b", r"\bhuman\b"
    ],
    "Abstract": [
        r"\babstract\b", r"\bgradient\b", r"\bgeometric\b",
        r"\btexture\b", r"\bpattern\b", r"\bpoly\b", r"\bfluid\b"
    ],
}


def normalize_text(text: str) -> str:
    """Normalize text by replacing separators and non-alphanumeric chars with spaces."""
    return re.sub(r"[^a-zA-Z0-9]+", " ", text).lower()


def extract_detailed_image_metadata(file_path: Path) -> Dict[str, Any]:
    """
    Extract comprehensive metadata from image headers, EXIF tags, and PNG chunks.
    """
    metadata: Dict[str, Any] = {
        "text_chunks": {},
        "exif_tags": {},
        "has_camera_exif": False,
        "ai_generation_parameters": None,
    }

    try:
        with Image.open(file_path) as img:
            # 1. PNG / WebP Text Info Chunks
            if hasattr(img, "info") and img.info:
                for k, v in img.info.items():
                    if isinstance(v, str):
                        metadata["text_chunks"][k] = v
                        # Check for AI generation parameters
                        if k in ["parameters", "prompt", "workflow", "Comment", "sd-metadata"]:
                            metadata["ai_generation_parameters"] = v

            # 2. EXIF Data (JPEG, TIFF, WebP)
            exif_raw = img.getexif()
            if exif_raw:
                for tag_id, val in exif_raw.items():
                    tag_name = TAGS.get(tag_id, str(tag_id))
                    if isinstance(val, (str, int, float)):
                        metadata["exif_tags"][tag_name] = str(val)

                # Check for camera hardware signatures
                camera_keys = ["Make", "Model", "FNumber", "ExposureTime", "ISOSpeedRatings", "FocalLength"]
                if any(k in metadata["exif_tags"] for k in camera_keys):
                    metadata["has_camera_exif"] = True

    except Exception:
        pass

    return metadata


def classify_ai(
    file_path: Path,
    source: Optional[str] = None,
    source_url: Optional[str] = None,
    tags: Optional[List[str]] = None,
    metadata_hint: Optional[Dict] = None,
) -> Tuple[str, float, str]:
    """
    Classify whether an image is AI, NON-AI, or UNKNOWN with confidence score.
    Returns (classification, confidence, detected_signal).
    """
    hint_type = (metadata_hint or {}).get("type")
    if hint_type in TYPES:
        return hint_type, 1.0, f"Explicit type hint: {hint_type}"

    # Extract deep file metadata
    img_meta = extract_detailed_image_metadata(file_path)

    # 1. Embedded AI Prompt / Generation Parameters Check (Definitive AI)
    if img_meta.get("ai_generation_parameters"):
        param_str = str(img_meta["ai_generation_parameters"]).lower()
        if any(w in param_str for w in ["steps:", "sampler:", "cfg scale:", "seed:", "model:", "negative prompt:"]):
            return "AI", 0.99, "Embedded Stable Diffusion/WebUI generation parameters in PNG chunk"

    # Build searchable corpus
    tag_corpus = " ".join(tags or [])
    raw_text = f"{file_path.name} {file_path.parent.name} {source or ''} {source_url or ''} {tag_corpus}"
    text_chunks_str = " ".join(f"{k}: {v}" for k, v in img_meta.get("text_chunks", {}).items())
    exif_str = " ".join(f"{k}: {v}" for k, v in img_meta.get("exif_tags", {}).items())
    combined = normalize_text(f"{raw_text} {text_chunks_str} {exif_str}")

    # 2. Known AI Indicators (Filename, Source, Tags, Software)
    ai_patterns = [
        (r"\bskiddle\s+generated\b", "Skiddle AI Generator"),
        (r"\bmidjourney\b", "Midjourney tag/metadata"),
        (r"\bstable\s+diffusion\b", "Stable Diffusion tag/metadata"),
        (r"\bdall\s*e\b", "DALL-E signature"),
        (r"\bnovelai\b", "NovelAI generation tag"),
        (r"\bflux\s*1\b", "FLUX.1 AI model"),
        (r"\bsdxl\b", "SDXL model"),
        (r"\bcomfyui\b", "ComfyUI workflow metadata"),
        (r"\bautomatic1111\b", "Automatic1111 WebUI"),
        (r"\blexica\b", "Lexica AI repository"),
        (r"\bcivitai\b", "Civitai model platform"),
        (r"\bai\s+generated\b", "AI-generated source tag"),
        (r"\bai\s+art\b", "AI Art tag"),
        (r"\bprompt\s*:\s*", "Prompt syntax header"),
    ]

    for pat, label in ai_patterns:
        if re.search(pat, combined):
            return "AI", 0.95, f"AI indicator detected: {label}"

    # 3. Known NON-AI Indicators (Camera EXIF, Official Studios, Verified Stock Photo Portals)
    if img_meta.get("has_camera_exif"):
        make = img_meta["exif_tags"].get("Make", "Camera")
        model = img_meta["exif_tags"].get("Model", "")
        return "NON-AI", 0.95, f"Physical camera hardware EXIF ({make} {model})".strip()

    non_ai_patterns = [
        (r"\bunsplash\b", "Unsplash photography"),
        (r"\bpixabay\b", "Pixabay stock photo"),
        (r"\bpexels\b", "Pexels photography"),
        (r"\bcanon\b", "Canon photography"),
        (r"\bnikon\b", "Nikon photography"),
        (r"\bsony\s*alpha\b", "Sony Alpha camera"),
        (r"\bfujifilm\b", "Fujifilm camera"),
        (r"\bpokemon\b", "Official Pokémon franchise"),
        (r"\bpikachu\b", "Official Pokémon media"),
        (r"\bnintendo\b", "Nintendo media"),
        (r"\bendfield\b", "Arknights: Endfield official media"),
        (r"\bwuwa\b", "Wuthering Waves official media"),
        (r"\barknights\b", "Arknights official media"),
        (r"\btoei\s*animation\b", "Toei Animation studio"),
        (r"\bkyoto\s*animation\b", "Kyoto Animation studio"),
        (r"\bufotable\b", "Ufotable studio"),
        (r"\bghibli\b", "Studio Ghibli"),
    ]

    for pat, label in non_ai_patterns:
        if re.search(pat, combined):
            return "NON-AI", 0.90, f"NON-AI source/studio detected: {label}"

    # 4. Fallback to UNKNOWN when evidence is not conclusive
    return "UNKNOWN", 0.5, "Insufficient provenance data for definitive classification"


def classify_category(
    file_path: Path,
    category_hint: Optional[str] = None,
    source_url: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> str:
    """
    Assign one of the 25 official categories.
    """
    if category_hint:
        normalized_hint = category_hint.strip()
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
            "Animals": "Animals",
            "Comics": "Comics",
            "Digital Art": "Digital Art",
            "Horror": "Horror",
            "Military": "Military",
            "Minimalism": "Minimalism",
            "Music": "Music",
            "Pixel Art": "Pixel Art",
            "Sports": "Sports",
            "Vehicles": "Vehicles",
        }
        for cat in CATEGORIES:
            if normalized_hint.lower() == cat.lower():
                return cat
        if normalized_hint in synonyms:
            return synonyms[normalized_hint]

    tag_str = " ".join(tags or [])
    raw_text = f"{file_path.name} {file_path.parent.name} {source_url or ''} {tag_str}"
    text = normalize_text(raw_text)

    scores: Dict[str, int] = {cat: 0 for cat in CATEGORIES}

    for cat, patterns in CATEGORY_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text):
                scores[cat] += 1

    best_cat, best_score = max(scores.items(), key=lambda item: item[1])

    if best_score > 0:
        return best_cat

    # Visual Fallback: Use CLIP zero-shot vision model if available
    if is_vision_available():
        vision_scores = classify_image_visually(file_path, top_k=1)
        if vision_scores and vision_scores[0][1] >= 0.20:
            return vision_scores[0][0]

    return "Other"


def classify_image(
    file_path: Path,
    source: Optional[str] = None,
    source_url: Optional[str] = None,
    tags: Optional[List[str]] = None,
    category_hint: Optional[str] = None,
    metadata_hint: Optional[Dict] = None,
) -> ClassificationResult:
    """
    Perform full classification on an image file.
    """
    ai_type, confidence, signal = classify_ai(
        file_path,
        source=source,
        source_url=source_url,
        tags=tags,
        metadata_hint=metadata_hint
    )
    category = classify_category(
        file_path,
        category_hint=category_hint,
        source_url=source_url,
        tags=tags,
    )
    return ClassificationResult(
        type=ai_type,
        category=category,
        ai_confidence=confidence,
        detected_signals=signal,
    )
