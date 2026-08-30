# 🖼️ Curated 2K+ Wallpaper Collection

A hand-picked collection of **2K+ resolution** wallpapers organized across 25 clean categories, backed by a local automated scraping, deduplication, and classification agent.

---

## 📂 Repository Architecture

* **`Curated/`** *(Published in Git)*: Hand-selected 2K+ wallpapers committed and shared in this repository.
* **`Wallpapers/`** *(Local Library)*: Full local archive indexed by sequential database IDs and SQLite (`wallpapers.db`).

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

**Quality Standard**: Every wallpaper meets or exceeds **2K QHD resolution** (≥ 3,686,400 pixels, e.g. 2560×1440, 3440×1440, 3840×2160) across 16:9, 21:9 ultrawide, and portrait orientations.

---

## 🏷️ 25 Official Categories

| Category | Description / Examples |
|---|---|
| `Abstract` | Gradients, geometric shapes, 3D renders, fluid art |
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

## 🚀 Quick Start (Local Agent)

```bash
# Install dependencies
pip install -r requirements.txt

# Run automated collection across all 25 categories
python agent.py auto --run-once

# Check local library stats
python agent.py stats

# Publish a wallpaper to Git
cp Wallpapers/Anime/104.png Curated/Anime/104.png
git add Curated/
git commit -m "✨ Add curated Anime wallpaper"
git push origin main
```

---

## ⚖️ Sources & Disclaimers

Wallpapers are archived from public sources for personal theme customization and desktop archiving:

<div align="center">
  <table><tr><td>

[![Wallhaven](https://img.shields.io/badge/Wallhaven-6DFF89?style=for-the-badge&logo=&logoColor=white)](https://wallhaven.cc/)
[![Wallpapers Clan](https://img.shields.io/badge/Wallpapers_Clan-F39C12?style=for-the-badge&logo=&logoColor=white)](https://wallpapers-clan.com/)
[![Alpha Coders](https://img.shields.io/badge/Alpha_Coders-00A8E8?style=for-the-badge&logo=&logoColor=white)](https://alphacoders.com/)
[![Pixiv](https://img.shields.io/badge/Pixiv-0096FA?style=for-the-badge&logo=pixiv&logoColor=white)](https://www.pixiv.net/en/)
[![Unsplash](https://img.shields.io/badge/Unsplash-000000?style=for-the-badge&logo=unsplash&logoColor=white)](https://unsplash.com/)
[![ArtStation](https://img.shields.io/badge/ArtStation-13AFF0?style=for-the-badge&logo=artstation&logoColor=white)](https://artstation.com/)
[![DeviantArt](https://img.shields.io/badge/DeviantArt-05CC47?style=for-the-badge&logo=deviantart&logoColor=white)](https://deviantart.com/)
[![UHD Paper](https://img.shields.io/badge/UHD_Paper-4A148C?style=for-the-badge&logo=&logoColor=white)](https://www.uhdpaper.com/)

  </td></tr></table>
</div>

*If you are the copyright owner of any image in this repository and wish to request removal, please open a GitHub issue.*
