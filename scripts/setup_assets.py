#!/usr/bin/env python3
"""
Downloads necessary frontend assets (HTMX, Lucide icons, fonts) to ensure
the application is fully functional in an airgapped/offline environment,
complying with government policies against using third-party CDNs.
"""
import os
import urllib.request
from pathlib import Path

ASSETS = {
    "htmx.org": "https://unpkg.com/htmx.org@1.9.10/dist/htmx.min.js",
    "lucide.min.js": "https://unpkg.com/lucide@latest/dist/umd/lucide.min.js",
}

def download_assets():
    base_dir = Path(__file__).resolve().parent.parent
    static_dir = base_dir / "src" / "janseva" / "admin" / "static" / "js"
    static_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, url in ASSETS.items():
        filepath = static_dir / filename
        if filepath.exists():
            print(f"✅ {filename} already exists, skipping.")
            continue
            
        print(f"⬇️ Downloading {filename} from {url}...")
        try:
            urllib.request.urlretrieve(url, filepath)
            print(f"✅ Downloaded {filename} to {filepath}")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")

if __name__ == "__main__":
    print("--- JanSeva Static Asset Setup ---")
    download_assets()
    print("--- Done ---")
