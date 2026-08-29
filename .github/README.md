# 🖼️ Wallpaper Collection & Agent

An automated, deduplicated, and classified wallpaper library adhering to strict **2K+ resolution** requirements, permanent database IDs, and structured filesystem organization.

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

---

## 📊 Collection Summary

* **Total 2K+ Wallpapers**: 311
* **Total Library Size**: 1.10 GB
* **Average Resolution**: 3869 × 2220 px
* **Min Resolution Standard**: ≥ 3,686,400 pixels (2560 × 1440)

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Check stats
python agent.py stats

# Download 2K+ wallpapers from Wallhaven
python agent.py wallhaven --query "cyberpunk" --limit 5

# Process incoming folder
python agent.py process
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
