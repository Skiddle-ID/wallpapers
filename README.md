# 🖼️ Curated 2K+ Wallpaper Collection

A hand-picked and curated collection of **2K+ resolution** wallpapers organized by clean categories, backed by a local automated archiving and classification agent.

---

## 📂 Architecture

* **`Curated/`** *(Tracked in Git)*: High-quality, manually curated wallpapers published to the repository.
* **`Wallpapers/`** *(Local Library)*: Full local archive indexed with SQLite (`wallpapers.db`) and sequential database IDs.

```text
Curated/
├── Abstract/
├── Animals/
├── Anime/
├── Architecture/
├── Cars/
├── City/
├── Comics/
├── Cyberpunk/
├── Digital Art/
├── Fantasy/
├── Gaming/
├── Horror/
├── Landscape/
├── Military/
├── Minimalism/
├── Music/
├── Nature/
├── Ocean/
├── People/
├── Pixel Art/
├── Sci-Fi/
├── Space/
├── Sports/
├── Vehicles/
└── Other/
```
├── Minimalism/
├── Music/
├── Nature/
├── Ocean/
├── People/
├── Pixel Art/
├── Sci-Fi/
├── Space/
├── Sports/
├── Vehicles/
└── Other/
```

**File Naming**: Sequential permanent ID (e.g. `Wallpapers/Anime/104.png`, `Wallpapers/Cyberpunk/315.png`).

---

## 🏷️ 25 Official Categories

| Category | Description / Examples |
|---|---|
| `Abstract` | Gradients, geometric, 3D shapes, fluid art |
| `Animals` | Wildlife, cats, dogs, wolves, birds, marine life |
| `Anime` | Anime, manga, waifu, chibi, Ghibli |
| `Architecture` | Bridges, temples, cathedrals, modern structures |
| `Cars` | Supercars, racing, sports cars, drift |
| `City` | Skylines, Tokyo streets, urban nightscapes |
| `Comics` | Marvel, DC, superheroes, Batman, Spider-Man |
| `Cyberpunk` | Neon cities, synthwave, futuristic metropolis |
| `Digital Art` | Concept art, CGI, ArtStation illustrations |
| `Fantasy` | Castles, dragons, mythical creatures, magic |
| `Gaming` | Video game art, characters, esports |
| `Horror` | Gothic art, dark fantasy, skulls, monsters |
| `Landscape` | Mountains, lakes, rivers, sunsets, horizons |
| `Military` | Fighter jets, naval ships, aviation, armor |
| `Minimalism` | Flat vector art, OLED/AMOLED, clean geometry |
| `Music` | Instruments, concerts, guitars, synth |
| `Nature` | Forests, plants, waterfalls, flowers, jungle |
| `Ocean` | Beaches, coastal waves, underwater coral |
| `People` | Portraits, models, human photography |
| `Pixel Art` | 8-bit, 16-bit, retro arcade scenery, voxels |
| `Sci-Fi` | Spaceships, robots, aliens, futuristic tech |
| `Space` | Galaxies, nebulas, solar systems, planets |
| `Sports` | Basketball, skateboarding, surfing, athletics |
| `Vehicles` | Motorcycles, aircraft, trains, yachts |
| `Other` | Miscellaneous high-resolution art |

---

## ⚙️ Pipeline & Features

Every ingested wallpaper undergoes automated processing:

```text
Incoming Wallpaper / Automated Stream
        ↓
Image Validation (Decode & Integrity)
        ↓
Resolution Check (≥ 2K / 3,686,400 px)
 ├── Under 2K → Rejected
 └── Valid 2K+
        ↓
Duplicate Detection
 ├── Exact SHA-256 Match → Rejected
 └── Perceptual Hash (pHash) → Checked
        ↓
AI Classification & Provenance Tracking (AI / NON-AI / UNKNOWN)
        ↓
Category Assignment (25 Categories + CLIP Vision Fallback)
        ↓
Assign Sequential Permanent Database ID
        ↓
Save as Wallpapers/<Category>/<ID>.<ext>
        ↓
Persist Metadata in SQLite (wallpapers.db)
```

---

## 🚀 CLI Usage

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. View Statistics
```bash
python agent.py stats
```

### 3. Automated Collection Daemon
Run the automated collector across all 25 categories configured in `collector_config.json`:

```bash
# Run one full multi-topic collection cycle (10 wallpapers per topic)
python agent.py auto --run-once

# Collect custom number of wallpapers per topic (e.g. 15 per topic)
python agent.py auto --limit 15 --run-once

# Run continuous collection daemon (every 1 hour)
python agent.py auto --interval 3600
```

### 4. Manual Wallhaven Search & Download
```bash
# Download top monthly wallpapers for any query
python agent.py wallhaven --query "cyberpunk" --limit 10 --sort toplist --top-range 1M

# Collect 2K+ Anime wallpapers
python agent.py wallhaven --query "anime girl" --limit 5 --category Anime

# Download a specific Wallhaven wallpaper by ID or URL
python agent.py wallhaven --id 1k7j9w
```

### 5. Process Incoming Directory
Drop local images into `incoming/` and run:
```bash
python agent.py process
```

### 6. Search Collection
```bash
python agent.py search --category Space --min-width 3840
```

### 7. Reclassify & Reorganize Existing Library
Re-evaluate existing wallpapers using updated metadata & CLIP vision rules:

```bash
# Preview reclassification changes
python agent.py reclassify --dry-run

# Apply reclassification and move files to updated folders
python agent.py reclassify
```

### 8. Verify Filesystem Integrity
```bash
python agent.py verify
```

---

## 🗄️ Database Schema (`wallpapers.db`)

The SQLite database acts as the single source of truth:

| Field | Type | Description |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY` | Sequential permanent ID |
| `filename` | `TEXT` | ID filename (e.g. `104.png`) |
| `type` | `TEXT` | `AI`, `NON-AI`, or `UNKNOWN` metadata |
| `category` | `TEXT` | One of the 25 official categories |
| `width` | `INTEGER` | Pixel width |
| `height` | `INTEGER` | Pixel height |
| `format` | `TEXT` | Image format (JPEG, PNG, WEBP) |
| `filesize` | `INTEGER` | Size in bytes |
| `sha256` | `TEXT UNIQUE` | Cryptographic hash |
| `perceptual_hash` | `TEXT` | pHash for visual similarity |
| `source` | `TEXT` | Source platform / uploader |
| `source_url` | `TEXT` | Original source webpage URL |
| `aspect_ratio` | `TEXT` | Common ratio (e.g. `16:9`, `21:9`) |
| `orientation` | `TEXT` | `Landscape`, `Portrait`, `Ultrawide`, `Square` |
| `created_at` | `TIMESTAMP` | Record timestamp |

---

## ⚖️ Disclaimer

All wallpapers are collected from public sources for personal archiving and theme customization. If you own an image and request removal, please open an issue.
