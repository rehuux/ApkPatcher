#!/usr/bin/env python3
import os
import shutil
import zipfile
from pathlib import Path

class SplitHandler:
    def __init__(self):
        self.name = "Split Handler"
    
    def merge_splits(self, split_dir):
        """Merge split APKs into single APK"""
        print(f"[+] Merging split APKs...")
        
        split_dir = Path(split_dir)
        if not split_dir.exists():
            print("[-] Split directory not found")
            return None
        
        # Find all split APKs
        split_files = list(split_dir.glob("*.apk"))
        if len(split_files) <= 1:
            print("[-] No split APKs found")
            return str(split_files[0]) if split_files else None
        
        # Merge splits
        merged_path = split_dir / "merged.apk"
        with zipfile.ZipFile(merged_path, 'w') as merged:
            for split_file in split_files:
                with zipfile.ZipFile(split_file, 'r') as split:
                    for item in split.namelist():
                        # Skip manifest if already added
                        if item == "AndroidManifest.xml" and item in merged.namelist():
                            continue
                        merged.writestr(item, split.read(item))
        
        print(f"[+] Merged splits to: {merged_path}")
        return str(merged_path)
    
    def extract_base(self, split_dir):
        """Extract base APK from splits"""
        split_dir = Path(split_dir)
        base_file = split_dir / "base.apk"
        if base_file.exists():
            return str(base_file)
        return None
