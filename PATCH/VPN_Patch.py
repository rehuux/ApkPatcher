#!/usr/bin/env python3
import os
import re
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "VPN Patch"
        self.description = "Remove VPN Detection"
    
    def apply(self, decompiled_dir, args):
        """Remove VPN detection"""
        print(f"[+] Applying {self.name}")
        
        smali_dir = Path(decompiled_dir) / "smali"
        if not smali_dir.exists():
            print("[-] smali directory not found")
            return False
        
        # VPN detection patterns
        vpn_patterns = [
            r'Landroid/net/ConnectivityManager;->getNetworkCapabilities',
            r'Landroid/net/NetworkCapabilities;->hasTransport',
            r'Ljava/net/NetworkInterface;->getNetworkInterfaces',
            r'Landroid/net/ConnectivityManager;->getAllNetworks',
            r'Landroid/net/ConnectivityManager;->getActiveNetwork',
            r'Landroid/net/ConnectivityManager;->getNetworkInfo',
            r'Landroid/net/NetworkCapabilities;->getTransportInfo'
        ]
        
        patched_count = 0
        for smali_file in smali_dir.rglob("*.smali"):
            try:
                with open(smali_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                modified = False
                for pattern in vpn_patterns:
                    if re.search(pattern, content):
                        # Return null/false
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
