#!/usr/bin/env python3
import os
import zipfile
import json
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "Flutter SSL Patch"
        self.description = "Bypass SSL Pinning in Flutter apps"
    
    def apply(self, decompiled_dir, args):
        """Apply Flutter SSL bypass"""
        print(f"[+] Applying {self.name}")
        
        # Check if it's a Flutter app
        lib_dir = Path(decompiled_dir) / "lib"
        if not lib_dir.exists():
            print("[-] Not a Flutter app (lib dir not found)")
            return False
        
        # Find libflutter.so
        flutter_libs = list(lib_dir.rglob("libflutter.so"))
        if not flutter_libs:
            print("[-] libflutter.so not found")
            return False
        
        print(f"[+] Found libflutter.so at: {flutter_libs[0]}")
        
        # Generate Frida script for Flutter
        frida_script = self.generate_frida_script()
        
        # Save script
        output_dir = Path(args.output) if hasattr(args, 'output') else Path("output")
        output_dir.mkdir(exist_ok=True)
        script_path = output_dir / "flutter_ssl_bypass.js"
        
        with open(script_path, 'w') as f:
            f.write(frida_script)
        
        print(f"[+] Frida script generated: {script_path}")
        print("[+] Run: frida -U -f <package> -l flutter_ssl_bypass.js")
        
        return True
    
    def generate_frida_script(self):
        """Generate Frida script for Flutter SSL bypass"""
        return """
// Flutter SSL Bypass Script
// Works on most Flutter apps

Java.perform(function() {
    console.log("[+] Flutter SSL Bypass Active");
    
    // Bypass Certificate Pinner
    var CertificatePinner = Java.use('okhttp3.CertificatePinner');
    CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function() {
        console.log("[+] Bypassing certificate pinning");
        return;
    };
    
    // Bypass Hostname Verifier
    var HostnameVerifier = Java.use('javax.net.ssl.HostnameVerifier');
    HostnameVerifier.verify.implementation = function(hostname, session) {
        console.log("[+] Bypassing hostname verification: " + hostname);
        return true;
    };
    
    // Bypass SSL Socket Factory
    var SSLSocketFactory = Java.use('javax.net.ssl.SSLSocketFactory');
    SSLSocketFactory.createSocket.overload('java.net.Socket', 'java.lang.String', 'int', 'boolean').implementation = function() {
        console.log("[+] Bypassing SSL socket");
        return this.createSocket();
    };
    
    // Bypass X509 TrustManager
    var TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    TrustManager.checkServerTrusted.implementation = function(certs, authType) {
        console.log("[+] Bypassing server trust check");
        return;
    };
    
    // Bypass Network Security Config (Flutter specific)
    var NetworkSecurityConfig = Java.use('android.security.net.config.NetworkSecurityConfig');
    NetworkSecurityConfig.isCleartextTrafficPermitted.implementation = function() {
        console.log("[+] Allowing cleartext traffic");
        return true;
    };
});
"""
