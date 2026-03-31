import requests
import base64
import time

# YOUR NVIDIA KEY (OLD ONE)
API_KEY = "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"
IMG_PATH = r"C:/Users/91741/.gemini/antigravity/brain/3261fd0e-7d3d-4413-a7e9-519816b4fa28/ruined_artifact_test_jpg_1774690829768.png"

def test_nvidia_trellis():
    print("--- [TEST] OFFICIAL MSFT TRELLIS PROBE ---")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    with open(IMG_PATH, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode('utf-8')

    # Try Image-to-3D payload
    payload = {
        "image": f"data:image/png;base64,{img_b64}",
        "output_format": "glb"
    }
    
    print("Step 1: Connecting to ai.api.nvidia.com...")
    url = "https://ai.api.nvidia.com/v1/genai/microsoft/trellis"
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f"Response: {r.status_code}")
    print(f"Body: {r.text[:500]}...")

    if r.status_code in [200, 201, 202]:
        print("SUCCESS! Endpoint is ACTIVE for this key.")
        if r.status_code == 202:
            print("Status: 202 Accepted (Polling required)")
        else:
            print("Status: 200/201 (Instant Result)")

if __name__ == "__main__":
    test_nvidia_trellis()
