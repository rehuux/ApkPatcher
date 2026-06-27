#!/usr/bin/env python3
import os
import re
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "USB Patch"
        self.description = "Hide USB Debugging Detection"
    
    def apply(self, decompiled_dir, args):
        """Hide USB debugging detection"""
        print(f"[+] Applying {self.name}")
        
        smali_dir = Path(decompiled_dir) / "smali"
        if not smali_dir.exists():
            print("[-] smali directory not found")
            return False
        
        # USB debugging patterns
        usb_patterns = [
            r'Landroid/os/Debug;->isDebuggerConnected',
            r'Landroid/os/Environment;->getExternalStorageDirectory',
            r'Landroid/os/Build;->getSerial',
            r'Landroid/app/ActivityThread;->currentActivityThread',
            r'Landroid/os/Debug;->waitingForDebugger',
            r'Landroid/os/Debug;->isDebuggerConnected'
        ]
        
        patched_count = 0
        for smali_file in smali_dir.rglob("*.smali"):
            try:
                with open(smali_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                modified = False
                for pattern in usb_patterns:
                    if re.search(pattern, content):
                        # Return false/empty
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
