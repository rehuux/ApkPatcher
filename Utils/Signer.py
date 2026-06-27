#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

class APKSigner:
    def __init__(self):
        self.keystore_path = "patcher.keystore"
        self.keystore_pass = "patcher123"
        self.key_alias = "patcher_key"
        self.generate_keystore()
    
    def generate_keystore(self):
        """Generate keystore if not exists"""
        if os.path.exists(self.keystore_path):
            return
        
        try:
            subprocess.run([
                'keytool', '-genkey', '-v',
                '-keystore', self.keystore_path,
                '-alias', self.key_alias,
                '-keyalg', 'RSA',
                '-keysize', '2048',
                '-validity', '10000',
                '-storepass', self.keystore_pass,
                '-keypass', self.keystore_pass,
                '-dname', 'CN=Test, OU=Test, O=Test, L=Test, ST=Test, C=IN'
            ], check=True, capture_output=True)
            print("[+] Generated keystore")
        except:
            print("[-] Failed to generate keystore")
    
    def sign_apk(self, apk_path):
        """Sign APK with keystore"""
        try:
            subprocess.run([
                'jarsigner', '-verbose',
                '-sigalg', 'SHA1withRSA',
                '-digestalg', 'SHA1',
                '-keystore', self.keystore_path,
                '-storepass', self.keystore_pass,
                '-keypass', self.keystore_pass,
                apk_path, self.key_alias
            ], check=True, capture_output=True)
            
            print(f"[+] Signed: {apk_path}")
            return apk_path
        except subprocess.CalledProcessError as e:
            print(f"[-] Signing error: {e.stderr.decode()}")
            return apk_path
    
    def zipalign(self, apk_path):
        """Zipalign APK for optimization"""
        aligned_path = apk_path.replace('.apk', '_aligned.apk')
        
        try:
            subprocess.run([
                'zipalign', '-v', '-p',
                '4', apk_path, aligned_path
            ], check=True, capture_output=True)
            
            print(f"[+] Zipaligned: {aligned_path}")
            return aligned_path
        except:
            print("[-] Zipalign failed, using unsigned APK")
            return apk_path
