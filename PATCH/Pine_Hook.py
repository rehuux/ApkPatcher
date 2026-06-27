#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "Pine Hook"
        self.description = "Pine hooking framework integration"
    
    def apply(self, decompiled_dir, args):
        """Integrate Pine hooking framework"""
        print(f"[+] Applying {self.name}")
        
        # Copy Pine files to decompiled directory
        pine_dir = Path(__file__).parent.parent / "Utils" / "Pine"
        if not pine_dir.exists():
            print("[-] Pine directory not found")
            return False
        
        # Copy PineCore to smali
        smali_dir = Path(decompiled_dir) / "smali"
        if smali_dir.exists():
            pine_smali_dir = smali_dir / "pine"
            pine_smali_dir.mkdir(exist_ok=True)
            
            # Copy Pine files
            for file in pine_dir.glob("*.smali"):
                shutil.copy(file, pine_smali_dir / file.name)
                print(f"[+] Copied {file.name} to smali")
        
        # Generate Frida script for Pine hooks
        pine_script = self.generate_pine_script()
        output_dir = Path(args.output) if hasattr(args, 'output') else Path("output")
        output_dir.mkdir(exist_ok=True)
        script_path = output_dir / "pine_hook.js"
        
        with open(script_path, 'w') as f:
            f.write(pine_script)
        
        print(f"[+] Pine hook script saved: {script_path}")
        print("[+] Run: frida -U -f <package> -l pine_hook.js")
        
        return True
    
    def generate_pine_script(self):
        """Generate Pine hook Frida script"""
        return """
// Pine Hook Framework
Java.perform(function() {
    console.log("[+] Pine Hook Framework Loaded");
    
    // Hook everything
    var Hook = Java.use('pine.Hook');
    
    // Hook PackageManager
    var PackageManager = Java.use('android.app.ApplicationPackageManager');
    PackageManager.getPackageInfo.implementation = function() {
        console.log("[+] Pine: getPackageInfo called");
        return this.getPackageInfo();
    };
    
    // Hook ActivityManager
    var ActivityManager = Java.use('android.app.ActivityManager');
    ActivityManager.getRunningAppProcesses.implementation = function() {
        console.log("[+] Pine: getRunningAppProcesses called");
        return null;
    };
    
    // Hook SystemProperties
    var SystemProperties = Java.use('android.os.SystemProperties');
    SystemProperties.get.overload('java.lang.String').implementation = function(key) {
        console.log("[+] Pine: SystemProperties.get(" + key + ")");
        if (key === 'ro.debuggable') return '1';
        if (key === 'ro.build.type') return 'userdebug';
        return this.get(key);
    };
    
    console.log("[+] Pine hooks applied!");
});
"""
