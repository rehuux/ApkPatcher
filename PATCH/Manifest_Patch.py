#!/usr/bin/env python3
import os
import re
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "Manifest Patch"
        self.description = "Modify AndroidManifest.xml"
    
    def apply(self, decompiled_dir, args):
        """Apply manifest modifications"""
        print(f"[+] Applying {self.name}")
        
        manifest_path = Path(decompiled_dir) / "AndroidManifest.xml"
        if not manifest_path.exists():
            print("[-] AndroidManifest.xml not found")
            return False
        
        # Read manifest
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add debuggable flag
        if 'android:debuggable="true"' not in content:
            content = content.replace(
                '<application ',
                '<application android:debuggable="true" '
            )
            print("[+] Added debuggable flag")
        
        # Add network security config
        if 'android:networkSecurityConfig' not in content:
            content = content.replace(
                '<application ',
                '<application android:networkSecurityConfig="@xml/network_security_config" '
            )
            print("[+] Added network security config")
        
        # Remove FLAG_SECURE (screenshot restriction)
        if 'android:secureFlag' in content:
            content = re.sub(r'android:secureFlag="[^"]*"', '', content)
            print("[+] Removed FLAG_SECURE")
        
        # Add all permissions
        permissions = [
            'android.permission.INTERNET',
            'android.permission.ACCESS_NETWORK_STATE',
            'android.permission.WRITE_EXTERNAL_STORAGE',
            'android.permission.READ_EXTERNAL_STORAGE',
            'android.permission.ACCESS_WIFI_STATE',
            'android.permission.ACCESS_COARSE_LOCATION',
            'android.permission.ACCESS_FINE_LOCATION'
        ]
        
        for perm in permissions:
            if perm not in content:
                content = content.replace(
                    '</manifest>',
                    f'    <uses-permission android:name="{perm}" />\n</manifest>'
                )
        
        # Write modified manifest
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Create network_security_config.xml
        self.create_network_config(decompiled_dir)
        
        print("[+] Manifest modified successfully")
        return True
    
    def create_network_config(self, decompiled_dir):
        """Create network security config for SSL bypass"""
        xml_dir = Path(decompiled_dir) / "res" / "xml"
        xml_dir.mkdir(parents=True, exist_ok=True)
        
        config_path = xml_dir / "network_security_config.xml"
        config_content = """<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
    </domain-config>
    <debug-overrides>
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
        </trust-anchors>
    </debug-overrides>
</network-security-config>
"""
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        print(f"[+] Created network_security_config.xml at {config_path}")
