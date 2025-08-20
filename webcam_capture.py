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

def upload_to_dropbox(image_data, filename):
    """Upload image to Dropbox App folder with date organization"""
    try:
        access_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
        
        if not access_token:
            print("❌ Dropbox access token not found")
            return False
        
        # Create date-based folder path
        date_folder = datetime.now().strftime('%Y-%m-%d')
        file_path = f"/{date_folder}/{filename}"
        
        upload_url = "https://content.dropboxapi.com/2/files/upload"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/octet-stream',
            'Dropbox-API-Arg': f'{{"path":"{file_path}","mode":"add","autorename":true}}'
        }
        
        response = requests.post(
            upload_url,
            headers=headers,
            data=image_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Uploaded to Dropbox: {file_path}")
            print(f"📏 Size: {result.get('size')} bytes")
            return True
        else:
            print(f"❌ Dropbox upload failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Dropbox upload error: {e}")
        return False

def fetch_and_save_image():
    timestamp = datetime.now()
    filename = f"hidden-lake-{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    
    # Add cache-busting timestamp
    target_url = f"{WEBCAM_URL}?t={int(time.time())}"
    
    for i, proxy_func in enumerate(PROXIES):
        try:
            url = proxy_func(target_url)
            print(f"Trying method {i+1}: {url[:100]}...")
            
            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                print(f"✅ Successfully fetched image: {filename}")
                print(f"📏 Image size: {len(response.content)} bytes")
                
                # Upload to Dropbox
                upload_success = upload_to_dropbox(response.content, filename)
                
                if upload_success:
                    return True
                else:
                    print("⚠️ Image fetched but upload failed")
                    return False
                    
            else:
                print(f"❌ Invalid response from method {i+1}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Method {i+1} failed: {str(e)}")
    
    print("❌ All methods failed")
    return False

def main():
    print(f"🏔️ Hidden Lake Webcam Capture → Dropbox")
    print(f"📅 {datetime.now()}")
    print("=" * 50)
    
    success = fetch_and_save_image()
    
    if success:
        print("✅ Capture and upload completed successfully!")
    else:
        print("❌ Capture failed!")
        exit(1)

if __name__ == "__main__":
    main()
