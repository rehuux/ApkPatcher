#!/usr/bin/env python3
import os
import re
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "Pairip CoreX"
        self.description = "Bypass Google Pairip Protection"
    
    def apply(self, decompiled_dir, args):
        """Bypass Pairip protection"""
        print(f"[+] Applying {self.name}")
        
        smali_dir = Path(decompiled_dir) / "smali"
        if not smali_dir.exists():
            print("[-] smali directory not found")
            return False
        
        # Pairip related patterns
        pairip_patterns = [
            (r'Lcom/google/android/pairip/PairipManager;->', 
             'Lcom/google/android/pairip/PairipManagerNOOP;->'),
            (r'Lcom/google/android/pairip/PairipVerifier;->', 
             'Lcom/google/android/pairip/PairipVerifierNOOP;->'),
            (r'invoke-virtual.*Lcom/google/android/pairip', 
             'invoke-virtual {v0}, Lnoop/Pairip;->'),
            (r'Lcom/google/android/pairip/PairipManager;->getInstance', 
             'Lcom/google/android/pairip/PairipManagerNOOP;->getInstance'),
            (r'Lcom/google/android/pairip/PairipVerifier;->verify', 
             'Lcom/google/android/pairip/PairipVerifierNOOP;->verify')
        ]
        
        patched_count = 0
        for smali_file in smali_dir.rglob("*.smali"):
            try:
                with open(smali_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                modified = False
                for pattern, replacement in pairip_patterns:
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
