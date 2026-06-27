#!/usr/bin/env python3
import os
import re
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "Package Patch"
        self.description = "Bypass package name checks"
    
    def apply(self, decompiled_dir, args):
        """Bypass package detection"""
        print(f"[+] Applying {self.name}")
        
        smali_dir = Path(decompiled_dir) / "smali"
        if not smali_dir.exists():
            print("[-] smali directory not found")
            return False
        
        # Package check patterns
        package_patterns = [
            r'Landroid/content/pm/PackageManager;->getPackageInfo',
            r'Landroid/content/pm/PackageManager;->getInstalledPackages',
            r'Landroid/content/pm/PackageManager;->getInstalledApplications',
            r'Landroid/app/ApplicationPackageManager;->getPackageInfo',
            r'Landroid/app/ApplicationPackageManager;->getInstalledPackages',
            r'Landroid/content/pm/PackageManager;->checkSignatures',
            r'Landroid/content/pm/PackageManager;->getPackageSignature'
        ]
        
        patched_count = 0
        for smali_file in smali_dir.rglob("*.smali"):
            try:
                with open(smali_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                modified = False
                for pattern in package_patterns:
                    if re.search(pattern, content):
                        # Return null/empty result
                        content = re.sub(pattern, pattern + 'NOOP', content)
                        modified = True
                
                if modified:
                    with open(smali_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    patched_count += 1
            except Exception as e:
                print(f"[-] Error patching {smali_file}: {e}")
        
        print(f"[+] Patched {patched_count} files")
        return True
