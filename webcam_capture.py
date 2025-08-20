#!/usr/bin/env python3
import requests
import time
import os
from datetime import datetime

# Configuration
WEBCAM_URL = "https://glacier.org/webcam/hlt_nps.jpg"

# Proxy services to try
PROXIES = [
    lambda url: f"https://api.cors.lol/?url={requests.utils.quote(url)}",
    lambda url: f"https://api.codetabs.com/v1/proxy?quest={requests.utils.quote(url)}",
    lambda url: f"https://cors-proxy.htmldriven.com/?url={requests.utils.quote(url)}",
    lambda url: url  # Direct attempt
]

def debug_environment():
    """Debug environment variables"""
    print("🔍 DEBUGGING ENVIRONMENT VARIABLES:")
    print("-" * 40)
    
    # Check if the token exists
    token = os.environ.get('DROPBOX_ACCESS_TOKEN')
    print(f"DROPBOX_ACCESS_TOKEN exists: {token is not None}")
    
    if token:
        print(f"Token length: {len(token)}")
        print(f"Token starts with: {token[:10]}...")
        print(f"Token type: {type(token)}")
    else:
        print("❌ Token is None or empty")
        
    # Show all environment variables that contain 'DROPBOX'
    dropbox_vars = {k: v for k, v in os.environ.items() if 'DROPBOX' in k.upper()}
    print(f"Environment variables containing 'DROPBOX': {list(dropbox_vars.keys())}")
    
    # Show all environment variables (first 10 chars of values for security)
    print("All environment variables:")
    for key in sorted(os.environ.keys()):
        value = os.environ[key]
        display_value = value[:10] + "..." if len(value) > 10 else value
        print(f"  {key}: {display_value}")
    
    print("-" * 40)

def upload_to_dropbox(image_data, filename):
    """Upload image to Dropbox App folder"""
    try:
        print("🔍 Starting Dropbox upload process...")
        
        access_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
        print(f"Token retrieved: {access_token is not None}")
        
        if not access_token:
            print("❌ Dropbox access token not found")
            
            # Try alternative ways to get the token
            alt_token = os.getenv('DROPBOX_ACCESS_TOKEN')
            print(f"Alternative os.getenv result: {alt_token is not None}")
            
            return False
        
        print(f"✅ Token found, length: {len(access_token)}")
        
        # Dropbox API upload endpoint
        upload_url = "https://content.dropboxapi.com/2/files/upload"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/octet-stream',
            'Dropbox-API-Arg': f'{{"path":"/{filename}","mode":"add","autorename":true}}'
        }
        
        print("📤 Sending request to Dropbox...")
        response = requests.post(
            upload_url,
            headers=headers,
            data=image_data,
            timeout=30
        )
        
        print(f"📥 Dropbox response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Uploaded to Dropbox: {filename}")
            print(f"📁 App folder path: {result.get('path_display')}")
            print(f"📏 Size: {result.get('size')} bytes")
            return True
        else:
            print(f"❌ Dropbox upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Dropbox upload error: {e}")
        return False

def fetch_and_save_image():
    timestamp = datetime.now()
    filename = f"hidden-lake-{timestamp.st
