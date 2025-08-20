#!/usr/bin/env python3
import requests
import time
import os
from datetime import datetime

# Configuration
WEBCAM_URL = "https://glacier.org/webcam/hlt_nps.jpg"
INTERVAL_SECONDS = 60  # Not used in GitHub Actions, but kept for reference

# Proxy services to try
PROXIES = [
    lambda url: f"https://api.cors.lol/?url={requests.utils.quote(url)}",
    lambda url: f"https://api.codetabs.com/v1/proxy?quest={requests.utils.quote(url)}",
    lambda url: f"https://cors-proxy.htmldriven.com/?url={requests.utils.quote(url)}",
    lambda url: url  # Direct attempt
]

def fetch_and_save_image():
    timestamp = datetime.now()
    filename = f"hidden-lake-{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    
    # Add cache-busting timestamp
    target_url = f"{WEBCAM_URL}?t={int(time.time())}"
    
    for i, proxy_func in enumerate(PROXIES):
        try:
            url = proxy_func(target_url)
            print(f"Trying method {i+1}: {url[:100]}...")
            
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                # For now, just print success (we'll add storage later)
                print(f"✅ Successfully fetched image: {filename}")
                print(f"📏 Image size: {len(response.content)} bytes")
                
                # You can add upload to cloud storage here later
                # save_to_cloud(response.content, filename)
                
                return True
            else:
                print(f"❌ Invalid response from method {i+1}")
                
        except Exception as e:
            print(f"❌ Method {i+1} failed: {str(e)}")
    
    print("❌ All methods failed")
    return False

def main():
    print(f"🏔️ Hidden Lake Webcam Capture - {datetime.now()}")
    print("=" * 50)
    
    success = fetch_and_save_image()
    
    if success:
        print("✅ Capture completed successfully!")
    else:
        print("❌ Capture failed!")
        exit(1)

if __name__ == "__main__":
    main()
