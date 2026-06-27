#!/usr/bin/env python3
import os
import subprocess
import shutil
from pathlib import Path

class APKTool:
    def __init__(self):
        self.apktool_path = "apktool"
    
    def decompile(self, apk_path):
        """Decompile APK to smali"""
        apk_name = Path(apk_path).stem
        output_dir = Path("decompiled_" + apk_name)
        
        # Clean previous
        if output_dir.exists():
            shutil.rmtree(output_dir)
        
        try:
            result = subprocess.run([
                self.apktool_path, 'd',
                apk_path,
                '-o', str(output_dir),
                '-f'
            ], check=True, capture_output=True)
            
            print(f"[+] Decompiled to: {output_dir}")
            return str(output_dir)
        except subprocess.CalledProcessError as e:
            print(f"[-] Decompile error: {e.stderr.decode()}")
            return None
    
    def rebuild(self, decompiled_dir, output_dir):
        """Rebuild APK from smali"""
        output_path = Path(output_dir) / "patched_app.apk"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            result = subprocess.run([
                self.apktool_path, 'b',
                decompiled_dir,
                '-o', str(output_path)
            ], check=True, capture_output=True)
            
            print(f"[+] Rebuilt: {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            print(f"[-] Rebuild error: {e.stderr.decode()}")
            return None
    
    def cleanup(self, decompiled_dir):
        """Remove temporary decompiled directory"""
        if os.path.exists(decompiled_dir):
            shutil.rmtree(decompiled_dir)
            print(f"[+] Cleaned: {decompiled_dir}")
