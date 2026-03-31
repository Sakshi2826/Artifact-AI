import requests
import json
import time

# YOUR NVIDIA KEY (OLD ONE)
API_KEY = "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"
IMG_PATH = r"C:/Users/91741/.gemini/antigravity/brain/3261fd0e-7d3d-4413-a7e9-519816b4fa28/ruined_artifact_test_jpg_1774690829768.png"

def test_nvidia_asset_flow():
    print("--- [TEST] NVIDIA ASSET PROTOCOL PROBE ---")
    headers = {"Authorization": f"Bearer {API_KEY}", "accept": "application/json"}
    
    # 1. CREATE ASSET
    print("Step 1: Creating Asset ID...")
    r = requests.post("https://api.nvcf.nvidia.com/v2/nvcf/assets", 
                      headers=headers, 
                      json={"contentType": "image/png", "description": "3D Specimen"}, 
                      timeout=20)
    print(f"Asset Init: {r.status_code}")
    if r.status_code != 200: 
        print(f"Error: {r.text}")
        return
    
    asset_data = r.json()
    asset_id = asset_data['assetId']
    upload_url = asset_data['uploadUrl']
    print(f"Asset ID: {asset_id}")

    # 2. UPLOAD
    print("Step 2: Uploading Binary...")
    with open(IMG_PATH, "rb") as f:
        r = requests.put(upload_url, data=f, headers={"Content-Type": "image/png"}, timeout=60)
    print(f"Upload Status: {r.status_code}")

    # 3. INFER
    print("Step 3: Inferring with Microsoft Trellis...")
    infer_url = "https://ai.api.nvidia.com/v1/genai/microsoft/trellis"
    # Testing both ways to be sure
    payload = {
        "image": f"https://api.nvcf.nvidia.com/v2/nvcf/assets/{asset_id}",
        "output_format": "glb"
    }
    
    # Wait a moment for S3 bucket sync
    time.sleep(2)
    r = requests.post(infer_url, headers=headers, json=payload, timeout=45)
    print(f"Infer Response: {r.status_code}")
    print(f"Infer Body: {r.text[:500]}")

if __name__ == "__main__":
    test_nvidia_asset_flow()
