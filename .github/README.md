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

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run automated collection across all 25 categories
python agent.py auto --run-once

# Start continuous collection daemon (every 1 hour)
python agent.py auto --interval 3600

# Check library stats
python agent.py stats
```

---

## ⚖️ Sources & Disclaimers

These images were collected for personal use from various public sources, including:

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

If you are the owner of any image and wish to have it removed, please open an issue.
