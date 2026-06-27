#!/usr/bin/env python3
import os
import re
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "Screenshot Patch"
        self.description = "Remove Screenshot Restriction"
    
    def apply(self, decompiled_dir, args):
        """Remove screenshot restriction"""
        print(f"[+] Applying {self.name}")
        
        # Modify AndroidManifest
        manifest_path = Path(decompiled_dir) / "AndroidManifest.xml"
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove FLAG_SECURE
            if 'android:secureFlag' in content:
                content = re.sub(r'android:secureFlag="[^"]*"', '', content)
                print("[+] Removed FLAG_SECURE from manifest")
            
            # Also remove window flags in smali
            smali_dir = Path(decompiled_dir) / "smali"
            if smali_dir.exists():
                window_patterns = [
                    r'Landroid/view/Window;->addFlags\(I\)V',
                    r'Landroid/view/WindowManager\$LayoutParams;->FLAG_SECURE',
                    r'Landroid/view/Window;->setFlags\(II\)V'
                ]
                
                for smali_file in smali_dir.rglob("*.smali"):
                    try:
                        with open(smali_file, 'r', encoding='utf-8', errors='ignore') as f:
                            content2 = f.read()
                        
                        modified = False
                        for pattern in window_patterns:
                            if re.search(pattern, content2):
                                # Remove FLAG_SECURE
                                content2 = re.sub(pattern, 'Lnoop/Window;', content2)
                                modified = True
                        
                        if modified:
                            with open(smali_file, 'w', encoding='utf-8') as f:
                                f.write(content2)
                    except Exception as e:
                        pass
            
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("[+] Screenshot restriction removed")
            return True
        
        print("[-] AndroidManifest.xml not found")
        return False
