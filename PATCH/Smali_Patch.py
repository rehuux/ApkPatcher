#!/usr/bin/env python3
import os
import re
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "Smali Patch"
        self.description = "Core smali code patching"
    
    def apply(self, decompiled_dir, args):
        """Apply smali patches"""
        print(f"[+] Applying {self.name}")
        
        smali_dir = Path(decompiled_dir) / "smali"
        if not smali_dir.exists():
            print("[-] smali directory not found")
            return False
        
        # SSL Pinning patterns - Smali instructions
        ssl_patterns = [
            # invoke-static patterns
            (r'invoke-static.*Ljavax/net/ssl/HttpsURLConnection;->setDefaultHostnameVerifier', 
             'invoke-static {v0}, Ljavax/net/ssl/HttpsURLConnection;->setDefaultHostnameVerifierNOOP'),
            
            # invoke-virtual patterns
            (r'invoke-virtual.*Lokhttp3/CertificatePinner;->check', 
             'invoke-virtual {v0}, Lokhttp3/CertificatePinner;->checkNOOP'),
            
            # invoke-static for TrustManager
            (r'invoke-static.*Ljavax/net/ssl/TrustManagerFactory;->getInstance', 
             'invoke-static {v0}, Ljavax/net/ssl/TrustManagerFactory;->getInstanceNOOP'),
            
            # invoke-virtual for OkHttp builder
            (r'invoke-virtual.*Lokhttp3/OkHttpClient\$Builder;->certificatePinner', 
             'invoke-virtual {v0}, Lokhttp3/OkHttpClient$Builder;->certificatePinnerNOOP'),
            
            # move-result instructions
            (r'move-result v0', 'move-result v0'),
            
            # if-eqz conditions (always false)
            (r'if-eqz v0, :cond_', 'if-eqz v0, :cond_NOOP'),
        ]
        
        patched_count = 0
        for smali_file in smali_dir.rglob("*.smali"):
            try:
                with open(smali_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                modified = False
                for pattern, replacement in ssl_patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        modified = True
                
                if modified:
                    with open(smali_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    patched_count += 1
            except Exception as e:
                print(f"[-] Error patching {smali_file}: {e}")
        
        print(f"[+] Patched {patched_count} smali files")
        return True
