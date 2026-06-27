#!/usr/bin/env python3
import os
import re
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "Ads Patch"
        self.description = "Remove advertisements"
    
    def apply(self, decompiled_dir, args):
        """Remove ads from app"""
        print(f"[+] Applying {self.name}")
        
        # Ad SDK patterns
        ad_patterns = [
            'com/google/android/gms/ads',
            'com/google/ads',
            'com/facebook/ads',
            'com/unity3d/ads',
            'com/applovin',
            'com/vungle',
            'com/ironsource',
            'com/adcolony',
            'com/chartboost',
            'com/inmobi',
            'com/mopub',
            'com/startapp',
            'com/admob',
            'com/advertising',
            'com/adMob',
            'com/amazon/ads',
            'com/verizon/ads'
        ]
        
        smali_dir = Path(decompiled_dir) / "smali"
        if not smali_dir.exists():
            print("[-] smali directory not found")
            return False
        
        patched_count = 0
        for smali_file in smali_dir.rglob("*.smali"):
            try:
                with open(smali_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                modified = False
                for pattern in ad_patterns:
                    if pattern in content:
                        # Replace with no-op
                        content = content.replace(pattern, 'Lnoop/ad')
                        modified = True
                
                if modified:
                    with open(smali_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    patched_count += 1
            except Exception as e:
                print(f"[-] Error patching {smali_file}: {e}")
        
        print(f"[+] Patched {patched_count} files")
        return True
