# 🖼️ Wallpaper Collection & Agent

An automated, deduplicated, and classified wallpaper library adhering to strict **2K+ resolution** requirements, permanent database IDs, and structured filesystem organization.

---

## 📊 Collection Statistics

* **Total 2K+ Wallpapers**: 317
* **Total Library Size**: 1.13 GB
* **Average Resolution**: 3871 × 2217 px
* **Min Resolution Standard**: ≥ 3,686,400 pixels (2560 × 1440)

### Classification Breakdown
* 🟢 **NON-AI**: 219 (69.1%)
* ⚪ **UNKNOWN**: 95 (30.0%)
* 🟣 **AI**: 3 (0.9%)

---

## 📂 Storage Architecture

Files are organized strictly by **Classification Type** and **Primary Category**, named after their permanent **Database ID**:

```text
Wallpapers/
├── AI/
│   ├── Anime/
│   ├── Architecture/
│   ├── Abstract/
│   ├── Cars/
│   ├── City/
│   ├── Cyberpunk/
│   ├── Fantasy/
│   ├── Gaming/
│   ├── Landscape/
│   ├── Nature/
│   ├── Ocean/
│   ├── People/
│   ├── Sci-Fi/
│   ├── Space/
│   └── Other/
│
├── NON-AI/
│   └── (15 categories)
│
└── UNKNOWN/
    └── (15 categories)
```

**File Naming**: Sequential permanent ID (e.g. `Wallpapers/NON-AI/Anime/104.png`).

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
AI Classification (AI / NON-AI / UNKNOWN)
        ↓
Category Assignment (15 Standard Categories)
        ↓
Assign Sequential Permanent Database ID
        ↓
Save as Wallpapers/<Type>/<Category>/<ID>.<ext>
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

### 3. Automated Daemon & Multi-Topic Collection
Run the automated collector across all topics configured in `collector_config.json`:

```bash
# Run one full multi-topic collection cycle
python agent.py auto --run-once

# Run continuous collection daemon (every 1 hour)
python agent.py auto --interval 3600

# Run with custom config
python agent.py auto --config my_topics.json
```

### 4. Manual Wallhaven Search & Download
```bash
# Download top 10 monthly wallpapers matching a query
python agent.py wallhaven --query "cyberpunk" --limit 10 --sort toplist --top-range 1M

# Collect 2K+ Anime wallpapers
python agent.py wallhaven --query "anime girl" --limit 5 --category Anime --type NON-AI

# Download a specific Wallhaven wallpaper by ID or URL
python agent.py wallhaven --id 1k7j9w
```

### 5. Process Incoming Directory
Drop local images into `incoming/` and run:
```bash
python agent.py process
```

### 6. Ingest Single File or URL
```bash
# Add local image
python agent.py add path/to/wallpaper.png

# Download and ingest from URL
python agent.py add "https://example.com/wallpaper.jpg" --type NON-AI --category Anime
```

### 7. Search Collection
```bash
python agent.py search --category Anime --min-width 3840
```

### 8. Verify Filesystem Integrity
```bash
python agent.py verify
```

---

## ⚙️ Configuration (`collector_config.json`)

Configure targets, queries, limits, and categories for automated ingestion:

```json
{
  "settings": {
    "delay_seconds": 1.5,
    "purity": "100",
    "min_resolution": "2560x1440",
    "default_limit_per_target": 5
  },
  "targets": [
    { "name": "Top Monthly", "query": null, "sorting": "toplist", "top_range": "1M", "limit": 5 },
    { "name": "Cyberpunk", "query": "cyberpunk", "sorting": "hot", "category_hint": "Cyberpunk", "limit": 5 },
    { "name": "Anime", "query": "anime", "sorting": "toplist", "category_hint": "Anime", "limit": 5 },
    { "name": "Landscape", "query": "landscape", "sorting": "toplist", "category_hint": "Landscape", "limit": 5 },
    { "name": "Space", "query": "space", "sorting": "toplist", "category_hint": "Space", "limit": 5 }
  ]
}
```

---

## 🗄️ Database Schema (`wallpapers.db`)

The SQLite database acts as the single source of truth:

| Field | Type | Description |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY` | Sequential permanent ID |
| `filename` | `TEXT` | ID filename (e.g. `104.png`) |
| `type` | `TEXT` | `AI`, `NON-AI`, or `UNKNOWN` |
| `category` | `TEXT` | One of the 15 standard categories |
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
