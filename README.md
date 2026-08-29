# 🖼️ Wallpaper Collection & Agent

An automated, deduplicated, and classified wallpaper library adhering to strict **2K+ resolution** requirements, permanent database IDs, and structured filesystem organization.

---

## 📊 Collection Statistics

* **Total 2K+ Wallpapers**: 311
* **Total Library Size**: 1.10 GB
* **Average Resolution**: 3869 × 2220 px
* **Min Resolution Standard**: ≥ 3,686,400 pixels (2560 × 1440)

### Classification Breakdown
* 🟢 **NON-AI**: 219 (70.4%)
* ⚪ **UNKNOWN**: 89 (28.6%)
* 🟣 **AI**: 3 (1.0%)

### Top Categories
* **Anime**: 222
* **Fantasy**: 13
* **Landscape**: 9
* **Nature**: 8
* **City**: 8
* **Space**: 6
* **Gaming**: 5
* **Architecture**: 2
* **Abstract**: 2
* **Cyberpunk**: 1
* **Ocean**: 1
* **Sci-Fi**: 1
* **Other**: 33

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
Incoming Wallpaper
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

### 3. Process Incoming Wallpapers
Drop files into `incoming/` and run:
```bash
python agent.py process
```

### 4. Ingest a Single File or URL
```bash
# Add local image
python agent.py add path/to/wallpaper.png

# Download and ingest from URL
python agent.py add "https://example.com/wallpaper.jpg" --type NON-AI --category Anime
```

### 5. Search Collection
```bash
python agent.py search --category Anime --min-width 3840
```

### 6. Verify Filesystem Integrity
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
| `type` | `TEXT` | `AI`, `NON-AI`, or `UNKNOWN` |
| `category` | `TEXT` | One of the 15 standard categories |
| `width` | `INTEGER` | Pixel width |
| `height` | `INTEGER` | Pixel height |
| `format` | `TEXT` | Image format (JPEG, PNG, WEBP) |
| `filesize` | `INTEGER` | Size in bytes |
| `sha256` | `TEXT UNIQUE` | Cryptographic hash |
| `perceptual_hash` | `TEXT` | pHash for visual similarity |
| `aspect_ratio` | `TEXT` | Common ratio (e.g. `16:9`, `21:9`) |
| `orientation` | `TEXT` | `Landscape`, `Portrait`, `Ultrawide`, `Square` |
| `created_at` | `TIMESTAMP` | Record timestamp |

---

## ⚖️ Disclaimer

All wallpapers are collected from public sources for personal archiving and theme customization. If you own an image and request removal, please open an issue.
