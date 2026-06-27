#!/usr/bin/env python3
import os
from pathlib import Path

class Patch:
    def __init__(self):
        self.name = "AES Logger"
        self.description = "Inject AES encryption logging"
    
    def apply(self, decompiled_dir, args):
        """Inject AES logging"""
        print(f"[+] Applying {self.name}")
        
        # Generate Frida script for AES logging
        aes_script = self.generate_aes_script()
        
        output_dir = Path(args.output) if hasattr(args, 'output') else Path("output")
        output_dir.mkdir(exist_ok=True)
        script_path = output_dir / "aes_logger.js"
        
        with open(script_path, 'w') as f:
            f.write(aes_script)
        
        print(f"[+] AES logger saved: {script_path}")
        print("[+] Run: frida -U -f <package> -l aes_logger.js")
        
        # Also inject smali file if available
        self.inject_smali_hooks(decompiled_dir)
        
        return True
    
    def generate_aes_script(self):
        """Generate AES logging Frida script"""
        return """
// AES Encryption/Decryption Logger
Java.perform(function() {
    console.log("[+] AES Logger Injected");
    
    // Hook Cipher
    var Cipher = Java.use('javax.crypto.Cipher');
    
    Cipher.doFinal.overload('[B').implementation = function(input) {
        console.log("[+] AES Operation:");
        console.log("    Input: " + bytesToHex(input));
        
        var result = this.doFinal(input);
        console.log("    Output: " + bytesToHex(result));
        
        return result;
    };
    
    // Hook SecretKeySpec
    var SecretKeySpec = Java.use('javax.crypto.spec.SecretKeySpec');
    SecretKeySpec.$init.overload('[B', 'java.lang.String').implementation = function(key, algorithm) {
        console.log("[+] AES Key Found:");
        console.log("    Algorithm: " + algorithm);
        console.log("    Key: " + bytesToHex(key));
        return this.$init(key, algorithm);
    };
    
    // Hook IvParameterSpec
    var IvParameterSpec = Java.use('javax.crypto.spec.IvParameterSpec');
    IvParameterSpec.$init.overload('[B').implementation = function(iv) {
        console.log("[+] AES IV Found:");
        console.log("    IV: " + bytesToHex(iv));
        return this.$init(iv);
    };
    
    // Hook KeyGenerator
    var KeyGenerator = Java.use('javax.crypto.KeyGenerator');
    KeyGenerator.generateKey.implementation = function() {
        var key = this.generateKey();
        console.log("[+] Generated Key: " + key);
        return key;
    };
    
    // Helper function
    function bytesToHex(bytes) {
        var hex = [];
        for (var i = 0; i < bytes.length; i++) {
            hex.push((bytes[i] >>> 4).toString(16));
            hex.push((bytes[i] & 0xF).toString(16));
        }
        return hex.join('');
    }
});
"""
    
    def inject_smali_hooks(self, decompiled_dir):
        """Inject smali hooks for AES logging"""
        smali_dir = Path(decompiled_dir) / "smali"
        if not smali_dir.exists():
            return
        
        # Create AES hook smali
        aes_smali = """.class public Laes/Hook;
.super Ljava/lang/Object;

.method public static log(Ljava/lang/String;[B)V
    .locals 3
    
    const-string v0, "AES_LOG"
    new-instance v1, Ljava/lang/StringBuilder;
    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V
    const-string v2, "AES: "
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v1
    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v1
    const-string v2, " - "
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v1
    invoke-static {p1}, Ljava/util/Arrays;->toString([B)Ljava/lang/String;
    move-result-object v2
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    move-result-object v1
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v1
    
    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
    
    return-void
.end method
"""
        
        # Save hook
        hook_dir = smali_dir / "aes"
        hook_dir.mkdir(exist_ok=True)
        hook_path = hook_dir / "Hook.smali"
        with open(hook_path, 'w') as f:
            f.write(aes_smali)
        
        print(f"[+] Injected AES hook at {hook_path}")
