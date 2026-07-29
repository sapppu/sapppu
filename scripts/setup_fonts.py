#!/usr/bin/env python3
import os
import sys
import urllib.request
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(HERE, "fonts")
os.makedirs(FONTS_DIR, exist_ok=True)

REGULAR_URL = "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf"
BOLD_URL = "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Bold.ttf"

reg_path = os.path.join(FONTS_DIR, "JetBrainsMono-Regular.ttf")
bold_path = os.path.join(FONTS_DIR, "JetBrainsMono-Bold.ttf")

def download(url, path):
    if os.path.exists(path):
        print(f"{os.path.basename(path)} already exists, skipping download.")
        return
    print(f"Downloading {url} to {path}...")
    urllib.request.urlretrieve(url, path)
    print("Download complete.")

def run_subset(font_path, text=None, unicodes=None, output_name=None):
    out_path = os.path.join(FONTS_DIR, output_name)
    cmd = [
        sys.executable, "-m", "fontTools.subset",
        font_path,
        "--flavor=woff2",
        "--layout-features=",
        "--no-hinting",
        f"--output-file={out_path}"
    ]
    if text:
        cmd.append(f"--text={text}")
    if unicodes:
        cmd.append(f"--unicodes={unicodes}")
        
    print(f"Subsetting {os.path.basename(font_path)} to {output_name}...")
    subprocess.run(cmd, check=True)
    print(f"Created {output_name} ({os.path.getsize(out_path) // 1024} KB)")

def main():
    download(REGULAR_URL, reg_path)
    download(BOLD_URL, bold_path)
    
    # 1. ramp subset (13 characters for the ASCII portrait)
    run_subset(reg_path, text=" .`:-=+*cs#%@", output_name="jbmono-ramp.woff2")
    
    # 2. headings subset (letters for headings)
    run_subset(reg_path, text="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ", output_name="jbmono-head.woff2")
    
    # 3. jbmono-400 (regular basic latin for statistics graphics)
    run_subset(reg_path, unicodes="U+0020-007E", output_name="jbmono-400.woff2")
    
    # 4. jbmono-600 (bold basic latin for statistics graphics)
    run_subset(bold_path, unicodes="U+0020-007E", output_name="jbmono-600.woff2")
    
    # Clean up large TTF files to keep the repo clean
    for path in [reg_path, bold_path]:
        if os.path.exists(path):
            os.remove(path)
            print(f"Removed temporary {os.path.basename(path)}")

if __name__ == "__main__":
    main()
