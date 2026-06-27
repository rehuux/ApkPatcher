#!/usr/bin/env python3
import os
import sys
import json
import logging
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from CLI import parse_arguments
from MODULES import ModuleManager
from Utils.Decompile_Compile import APKTool
from Utils.Signer import APKSigner
from Utils.Anti_Splits import SplitHandler
from Utils.CRC import CRCFixer

class APKPatcher:
    def __init__(self):
        self.config = self.load_config()
        self.setup_logging()
        self.module_manager = ModuleManager()
        self.apk_tool = APKTool()
        self.signer = APKSigner()
        self.split_handler = SplitHandler()
        self.crc_fixer = CRCFixer()
        
        # Colors
        self.GREEN = '\033[92m'
        self.RED = '\033[91m'
        self.YELLOW = '\033[93m'
        self.BLUE = '\033[94m'
        self.RESET = '\033[0m'
        
        self.decompiled_dir = None
        self.package_name = None
    
    def load_config(self):
        """Load configuration from config.json"""
        config_path = Path(__file__).parent / "config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {
            "keystore": {
                "path": "patcher.keystore",
                "password": "patcher123",
                "alias": "patcher_key"
            },
            "apktool": {
                "path": "apktool",
                "framework_dir": "~/.apktool/framework"
            },
            "logging": {
                "level": "INFO",
                "file": "patcher.log"
            }
        }
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.config.get("logging", {}).get("file", "patcher.log")
        log_level = self.config.get("logging", {}).get("level", "INFO")
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("APKPatcher")
    
    def print_banner(self):
        """Print banner"""
        banner = f"""
{self.GREEN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   █████╗ ██████╗ ██╗  ██╗██████╗  █████╗ ████████╗     ║
║  ██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗╚══██╔══╝     ║
║  ███████║██████╔╝█████╔╝ ██████╔╝███████║   ██║        ║
║  ██╔══██║██╔═══╝ ██╔═██╗ ██╔═══╝ ██╔══██║   ██║        ║
║  ██║  ██║██║     ██║  ██╗██║     ██║  ██║   ██║        ║
║  ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝        ║
║                                                          ║
║         Complete APK Patcher Tool v2.0                  ║
║         Educational Purpose Only                        ║
╚══════════════════════════════════════════════════════════╝{self.RESET}
        """
        print(banner)
    
    def run(self):
        """Main execution flow"""
        self.print_banner()
        
        # Parse CLI arguments
        args = parse_arguments()
        
        if not args.input:
            self.logger.error("No APK file specified! Use -i <apk_path>")
            print(f"{self.RED}Usage: python APK_PATCHER.py -i app.apk --all{self.RESET}")
            sys.exit(1)
        
        # Check if APK exists
        if not os.path.exists(args.input):
            self.logger.error(f"APK not found: {args.input}")
            sys.exit(1)
        
        self.logger.info(f"Starting patching process for: {args.input}")
        
        # Step 1: Handle split APK if needed
        if args.split:
            self.logger.info("Handling split APK...")
            merged_apk = self.split_handler.merge_splits(args.input)
            if merged_apk:
                args.input = merged_apk
        
        # Step 2: Decompile APK
        self.logger.info("Decompiling APK...")
        self.decompiled_dir = self.apk_tool.decompile(args.input)
        
        if not self.decompiled_dir:
            self.logger.error("Decompilation failed!")
            sys.exit(1)
        
        # Extract package name from manifest
        self.extract_package_name()
        
        # Step 3: Load and apply patches
        self.logger.info("Applying patches...")
        patches = self.module_manager.get_selected_patches(args)
        
        for patch_name, patch_module in patches:
            self.logger.info(f"Applying: {patch_name}")
            try:
                if hasattr(patch_module, 'apply'):
                    patch_module.apply(self.decompiled_dir, args)
                    self.logger.info(f"{self.GREEN}✅ {patch_name} applied successfully{self.RESET}")
                else:
                    self.logger.warning(f"⚠️ {patch_name} has no apply method")
            except Exception as e:
                self.logger.error(f"{self.RED}❌ {patch_name} failed: {e}{self.RESET}")
        
        # Step 4: Fix CRC if needed
        self.logger.info("Fixing CRC...")
        self.crc_fixer.fix(self.decompiled_dir)
        
        # Step 5: Rebuild APK
        self.logger.info("Rebuilding APK...")
        rebuilt_apk = self.apk_tool.rebuild(self.decompiled_dir, args.output)
        
        if not rebuilt_apk:
            self.logger.error("Rebuilding failed!")
            sys.exit(1)
        
        # Step 6: Sign APK
        self.logger.info("Signing APK...")
        signed_apk = self.signer.sign_apk(rebuilt_apk)
        
        # Step 7: Zipalign
        self.logger.info("Optimizing APK...")
        final_apk = self.signer.zipalign(signed_apk)
        
        # Step 8: Generate Magisk module if requested
        if args.magisk:
            self.logger.info("Generating Magisk module...")
            self.generate_magisk_module(final_apk)
        
        # Step 9: Generate Frida script if requested
        if args.frida:
            self.logger.info("Generating Frida script...")
            self.generate_frida_script()
        
        # Step 10: Cleanup
        self.logger.info("Cleaning up...")
        self.apk_tool.cleanup(self.decompiled_dir)
        
        self.logger.info(f"{self.GREEN}✅ Patching complete! Output: {final_apk}{self.RESET}")
        print(f"\n{self.GREEN}🎉 Success! Patched APK saved to: {final_apk}{self.RESET}")
    
    def extract_package_name(self):
        """Extract package name from AndroidManifest.xml"""
        manifest_path = Path(self.decompiled_dir) / "AndroidManifest.xml"
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
                import re
                match = re.search(r'package="([^"]+)"', content)
                if match:
                    self.package_name = match.group(1)
                    self.logger.info(f"Package: {self.package_name}")
    
    def generate_magisk_module(self, apk_path):
        """Generate Magisk module"""
        module_dir = Path("magisk_module")
        module_dir.mkdir(exist_ok=True)
        
        # module.prop
        with open(module_dir / "module.prop", 'w') as f:
            f.write(f"""
id=apkpatcher
name=APK Patcher Module
version=v1.0
versionCode=1
author=APKPatcher
description=Patched APK with modifications
""")
        
        # customize.sh
        with open(module_dir / "customize.sh", 'w') as f:
            f.write("""#!/system/bin/sh
ui_print "Installing patched APK..."
pm install -r /data/adb/modules/apkpatcher/patched_app.apk
ui_print "Done!"
""")
        
        # Copy APK
        shutil.copy(apk_path, module_dir / "patched_app.apk")
        
        # Create zip
        zip_path = Path("magisk_module.zip")
        import zipfile
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(module_dir):
                for file in files:
                    file_path = Path(root) / file
                    zipf.write(file_path, file_path.relative_to("."))
        
        self.logger.info(f"Magisk module: {zip_path}")
    
    def generate_frida_script(self):
        """Generate Frida script for runtime patching"""
        script_path = Path("frida_script.js")
        script_content = f"""
// Frida Script for {self.package_name if self.package_name else 'Unknown'}
// Generated by APK Patcher

Java.perform(function() {{
    console.log("[+] Frida Script Loaded");
    
    // SSL Bypass
    var CertificatePinner = Java.use('okhttp3.CertificatePinner');
    CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function() {{
        console.log("[+] Bypassing certificate pinning");
        return;
    }};
    
    // VPN Detection Bypass
    var ConnectivityManager = Java.use('android.net.ConnectivityManager');
    ConnectivityManager.getNetworkCapabilities.implementation = function() {{
        console.log("[+] Bypassing VPN detection");
        return null;
    }};
    
    // Debug Detection Bypass
    var Debug = Java.use('android.os.Debug');
    Debug.isDebuggerConnected.implementation = function() {{
        console.log("[+] Hiding debugger");
        return false;
    }};
    
    console.log("[+] All hooks applied successfully!");
}});
"""
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        self.logger.info(f"Frida script: {script_path}")
        self.logger.info("Run: frida -U -f PACKAGE -l frida_script.js")

if __name__ == "__main__":
    patcher = APKPatcher()
    patcher.run()
