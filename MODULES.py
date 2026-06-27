#!/usr/bin/env python3
import importlib
import importlib.util
import os
import sys
from pathlib import Path

class ModuleManager:
    def __init__(self):
        self.modules = {}
        self.load_all_modules()
    
    def load_all_modules(self):
        """Load all patch modules from Patch directory"""
        patch_dir = Path(__file__).parent / "Patch"
        
        if not patch_dir.exists():
            print(f"[-] Patch directory not found: {patch_dir}")
            return
        
        for file in patch_dir.glob("*.py"):
            if file.name.startswith("__"):
                continue
            
            module_name = file.stem
            try:
                # Dynamic import
                spec = importlib.util.spec_from_file_location(
                    f"Patch.{module_name}",
                    file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if module has Patch class or apply function
                if hasattr(module, 'Patch'):
                    self.modules[module_name] = module.Patch()
                elif hasattr(module, 'apply'):
                    self.modules[module_name] = module
                else:
                    self.modules[module_name] = module
                
                print(f"[+] Loaded module: {module_name}")
                
            except Exception as e:
                print(f"[-] Failed to load module {module_name}: {e}")
    
    def get_selected_patches(self, args):
        """Get patches based on CLI arguments"""
        selected = []
        
        # Map CLI flags to modules (as per your structure)
        patch_map = {
            'all': [
                'Smali_Patch', 'Flutter_SSL_Patch', 'Manifest_Patch',
                'Ads_Patch', 'AES', 'Spoof_Patch', 'Package',
                'Pairip_CoreX', 'Pine_Hook', 'VPN_Patch',
                'USB_Patch', 'Screenshot_Patch'
            ],
            'ssl': ['Smali_Patch'],
            'flutter': ['Flutter_SSL_Patch'],
            'vpn': ['VPN_Patch'],
            'usb': ['USB_Patch'],
            'remove_screenshot': ['Screenshot_Patch'],
            'ads': ['Ads_Patch'],
            'aes': ['AES'],
            'spoof': ['Spoof_Patch'],
            'package': ['Package'],
            'device': ['Spoof_Patch'],
            'pairip': ['Pairip_CoreX'],
            'pine': ['Pine_Hook']
        }
        
        if args.all:
            modules = patch_map['all']
        else:
            modules = []
            for flag, mods in patch_map.items():
                if hasattr(args, flag) and getattr(args, flag):
                    modules.extend(mods)
        
        # Remove duplicates
        modules = list(set(modules))
        
        # Get module objects
        for module_name in modules:
            if module_name in self.modules:
                selected.append((module_name, self.modules[module_name]))
            else:
                print(f"[-] Module not found: {module_name}")
        
        return selected
