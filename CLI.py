#!/usr/bin/env python3
import argparse
import sys

def parse_arguments():
    """Parse all command line arguments"""
    parser = argparse.ArgumentParser(
        description="APK Patcher - Complete Android APK Modding Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python APK_PATCHER.py -i app.apk -f -p -c
  python APK_PATCHER.py -i app.apk -f --ssl --vpn --ads
  python APK_PATCHER.py -i app.apk -P -rmss -rmusb
  python APK_PATCHER.py -i app.apk --flutter --aes -o modified/
        """
    )
    
    # Required arguments
    parser.add_argument(
        '-i', '--input',
        help='Input APK file path',
        required=False
    )
    
    parser.add_argument(
        '-o', '--output',
        default='patched_output',
        help='Output directory (default: patched_output)'
    )
    
    # Short options (as per your description)
    parser.add_argument(
        '-f', '--flutter',
        action='store_true',
        help='Bypass Flutter SSL Pinning'
    )
    
    parser.add_argument(
        '-p', '--package',
        action='store_true',
        help='Bypass Package Detection'
    )
    
    parser.add_argument(
        '-c', '--crc',
        action='store_true',
        help='Fix CRC'
    )
    
    parser.add_argument(
        '-P', '--pairip',
        action='store_true',
        help='Bypass Google Pairip Protection'
    )
    
    parser.add_argument(
        '-rmss', '--remove-screenshot',
        action='store_true',
        help='Remove Screenshot Restriction'
    )
    
    parser.add_argument(
        '-rmusb', '--remove-usb',
        action='store_true',
        help='Hide USB Debugging Detection'
    )
    
    # Feature flags (long options)
    parser.add_argument(
        '--all',
        action='store_true',
        help='Apply ALL patches'
    )
    
    parser.add_argument(
        '--ssl',
        action='store_true',
        help='Bypass SSL Pinning'
    )
    
    parser.add_argument(
        '--vpn',
        action='store_true',
        help='Remove VPN Detection'
    )
    
    parser.add_argument(
        '--ads',
        action='store_true',
        help='Remove Ads'
    )
    
    parser.add_argument(
        '--aes',
        action='store_true',
        help='Inject AES Logging'
    )
    
    parser.add_argument(
        '--spoof',
        action='store_true',
        help='Spoof Device Info'
    )
    
    parser.add_argument(
        '--device',
        action='store_true',
        help='Bypass One Device Login'
    )
    
    parser.add_argument(
        '--pine',
        action='store_true',
        help='Enable Pine Hook Framework'
    )
    
    parser.add_argument(
        '--split',
        action='store_true',
        help='Handle Split APK'
    )
    
    parser.add_argument(
        '--magisk',
        action='store_true',
        help='Generate Magisk Module'
    )
    
    parser.add_argument(
        '--frida',
        action='store_true',
        help='Generate Frida Script'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='APK Patcher v2.0'
    )
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    return args
