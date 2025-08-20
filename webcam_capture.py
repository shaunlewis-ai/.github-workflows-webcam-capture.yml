#!/usr/bin/env python3
import requests
import time
import os
from datetime import datetime

WEBCAM_URL = "https://glacier.org/webcam/hlt_nps.jpg"

PROXIES = [
    lambda url: f"https://api.cors.lol/?url={requests.utils.quote(url)}",
    lambda url: f"https://api.codetabs.com/v1/proxy?quest={requests.utils.quote(url)}",
    lambda url: f"https://cors-proxy.htmldriven.com/?url={requests.utils.quote(url)}",
    lambda url: url
]

def debug_environment():
    print("DEBUG: Checking environment variables")
    token = os.environ.get('DROPBOX_ACCESS_TOKEN')
    print(f"Token exists: {token is not None}")
    if token:
        print(f"Token length: {len(token)}")
        print(f"Token starts with: {token[:10]}...")
    else:
        print("ERROR: Token is None or empty")

def upload_to_dropbox(image_data, filename):
    try:
        print("Starting Dropbox upload...")
        
        access_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
        
        if not access_token:
            print("ERROR: Dropbox access token not found")
            return False
        
        print(f"Token found, length: {len(access_token)}")
        
        upload_url = "https://content.dropboxapi.com/2/files/upload"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/octet-stream',
            'Dropbox-API-Arg': f'{{"path":"/{filename}","mode":"add","autorename":true}}'
        }
        
        print("Sending request to Dropbox...")
        response = requests.post(upload_url, headers=headers, data=image_data, timeout=30)
        
        print(f"Dropbox response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: Uploaded {filename}")
            print(f"Path: {result.get('path_display')}")
            print(f"Size: {result.get('size')} bytes")
            return True
        else:
            print(f"ERROR: Dropbox upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: Dropbox upload exception: {e}")
        return False

def fetch_and_save_image():
    timestamp = datetime.now()
    filename = f"hidden-lake-{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    
    target_url = f"{WEBCAM_URL}?t={int(time.time())}"
    
    for i, proxy_func in enumerate(PROXIES):
        try:
            url = proxy_func(target_url)
            print(f"Trying method {i+1}: {url[:100]}...")
            
            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                print(f"SUCCESS: Fetched image: {filename}")
                print(f"Image size: {len(response.content)} bytes")
                
                upload_success = upload_to_dropbox(response.content, filename)
                
                if upload_success:
                    return True
                else:
                    print("WARNING: Image fetched but upload failed")
                    return False
                    
            else:
                print(f"ERROR: Invalid response from method {i+1}: {response.status_code}")
                
        except Exception as e:
            print(f"ERROR: Method {i+1} failed: {str(e)}")
    
    print("ERROR: All methods failed")
    return False

def main():
    print("Hidden Lake Webcam Capture to Dropbox")
    print(f"Date: {datetime.now()}")
    print("=" * 50)
    
    debug_environment()
    
    success = fetch_and_save_image()
    
    if success:
        print("SUCCESS: Capture and upload completed!")
    else:
        print("ERROR: Capture failed!")
        exit(1)

if __name__ == "__main__":
    main()
