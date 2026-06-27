#!/usr/bin/env python3
import os
import zlib
from pathlib import Path

class CRCFixer:
    def __init__(self):
        self.name = "CRC Fixer"
    
    def fix(self, decompiled_dir):
        """Fix CRC in decompiled files"""
        print(f"[+] Fixing CRC...")
        
        # Fix classes.dex CRC
        dex_path = Path(decompiled_dir) / "classes.dex"
        if dex_path.exists():
            self.fix_dex_crc(dex_path)
        
        # Fix AndroidManifest.xml CRC
        manifest_path = Path(decompiled_dir) / "AndroidManifest.xml"
        if manifest_path.exists():
            self.fix_file_crc(manifest_path)
        
        print("[+] CRC fix complete")
    
    def fix_dex_crc(self, dex_path):
        """Fix classes.dex CRC in apktool.yml"""
        yml_path = dex_path.parent / "apktool.yml"
        if not yml_path.exists():
            return
        
        with open(dex_path, 'rb') as f:
            data = f.read()
            crc = zlib.crc32(data) & 0xFFFFFFFF
        
        with open(yml_path, 'r') as f:
            content = f.read()
        
        # Update CRC in apktool.yml
        import re
        content = re.sub(r'crc:.*', f'crc: {crc}', content)
        
        with open(yml_path, 'w') as f:
            f.write(content)
        
        print(f"[+] Fixed CRC for classes.dex: {crc}")
    
    def fix_file_crc(self, file_path):
        """Fix CRC for any file"""
        with open(file_path, 'rb') as f:
            data = f.read()
            crc = zlib.crc32(data) & 0xFFFFFFFF
        print(f"[+] File CRC: {crc}")
