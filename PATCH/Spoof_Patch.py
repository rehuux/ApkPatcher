#!/usr/bin/env python3
import os
import re
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "Spoof Patch"
        self.description = "Spoof device info and bypass package detection"
    
    def apply(self, decompiled_dir, args):
        """Apply spoofing patches"""
        print(f"[+] Applying {self.name}")
        
        smali_dir = Path(decompiled_dir) / "smali"
        if not smali_dir.exists():
            print("[-] smali directory not found")
            return False
        
        # Device info patterns - Build class fields
        device_patterns = [
            (r'Landroid/os/Build;->MODEL', 'Landroid/os/Build;->MODEL_SPOOFED'),
            (r'Landroid/os/Build;->MANUFACTURER', 'Landroid/os/Build;->MANUFACTURER_SPOOFED'),
            (r'Landroid/os/Build;->DEVICE', 'Landroid/os/Build;->DEVICE_SPOOFED'),
            (r'Landroid/os/Build;->PRODUCT', 'Landroid/os/Build;->PRODUCT_SPOOFED'),
            (r'Landroid/os/Build;->BRAND', 'Landroid/os/Build;->BRAND_SPOOFED'),
            (r'Landroid/os/Build;->FINGERPRINT', 'Landroid/os/Build;->FINGERPRINT_SPOOFED'),
            (r'Landroid/os/Build;->SERIAL', 'Landroid/os/Build;->SERIAL_SPOOFED'),
            (r'Landroid/os/Build;->BOARD', 'Landroid/os/Build;->BOARD_SPOOFED')
        ]
        
        # Package detection patterns
        package_patterns = [
            (r'Landroid/app/ApplicationPackageManager;->getPackageInfo', 
             'Landroid/app/ApplicationPackageManager;->getPackageInfoNOOP'),
            (r'Landroid/app/ApplicationPackageManager;->getInstalledPackages', 
             'Landroid/app/ApplicationPackageManager;->getInstalledPackagesNOOP'),
            (r'Landroid/app/ActivityManager;->getRunningAppProcesses', 
             'Landroid/app/ActivityManager;->getRunningAppProcessesNOOP'),
            (r'Landroid/app/ActivityManager;->getRunningServices', 
             'Landroid/app/ActivityManager;->getRunningServicesNOOP'),
            (r'Landroid/os/Process;->getUidForName', 
             'Landroid/os/Process;->getUidForNameNOOP'),
            (r'Ljava/lang/Runtime;->exec', 
             'Ljava/lang/Runtime;->execNOOP')
        ]
        
        patched_count = 0
        for smali_file in smali_dir.rglob("*.smali"):
            try:
                with open(smali_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                modified = False
                
                # Apply device spoofing
                for pattern, replacement in device_patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        modified = True
                
                # Apply package detection bypass
                for pattern, replacement in package_patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        modified = True
                
                if modified:
                    with open(smali_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    patched_count += 1
            except Exception as e:
                print(f"[-] Error patching {smali_file}: {e}")
        
        print(f"[+] Patched {patched_count} files")
        return True
