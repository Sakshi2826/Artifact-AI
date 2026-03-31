import requests
import json
import time

# YOUR API KEY
API_KEY = "tsk_XglMcK6xezjvPDDNuCtItGhlSTyzIvC6SN6dA7k_ae4"
# A sample image for testing (Konark Temple from earlier)
IMG_PATH = r"C:/Users/91741/.gemini/antigravity/brain/3261fd0e-7d3d-4413-a7e9-519816b4fa28/ruined_artifact_test_jpg_1774690829768.png"

def test_tripo():
    print("--- [TEST] TRIPO AI PROBE STARTED ---")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # 1. UPLOAD
    print("Step 1: Uploading...")
    try:
        with open(IMG_PATH, "rb") as f:
            r = requests.post("https://api.tripo3d.ai/v2/openapi/upload", headers=headers, files={'file': f}, timeout=30)
        print(f"Upload Response: {r.status_code} - {r.text}")
        if r.status_code != 200: return
        token = r.json()['data']['image_token']
        print(f"Token: {token}")

        # 2. CREATE TASK
        print("Step 2: Creating Task...")
        p = {"type": "image_to_model", "file": {"type": "jpg", "file_token": token}}
        r = requests.post("https://api.tripo3d.ai/v2/openapi/task", headers=headers, json=p, timeout=20)
        print(f"Task Response: {r.status_code} - {r.text}")
        if r.status_code != 200: return
        task_id = r.json()['data']['task_id']
        print(f"Task ID: {task_id}")

        # 3. POLL (Briefly check status)
        print("Step 3: Polling status...")
        for i in range(3):
            time.sleep(5)
            r = requests.get(f"https://api.tripo3d.ai/v2/openapi/task/{task_id}", headers=headers).json()
            st = r.get('data', {}).get('status')
            print(f"Status ({i+1}): {st}")
            if st == 'success':
                print(f"SUCCESS! GLB URL: {r['data']['output']['model']}")
                return

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_tripo()
