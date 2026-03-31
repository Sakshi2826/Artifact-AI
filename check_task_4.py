import os, django, json, re, ast, requests, time, base64, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from analyzer.models import ArtifactTask
from django.conf import settings

def run():
    task = ArtifactTask.objects.get(id=4)
    print(f"Checking Task {task.id} with image {task.ruined_image.path}")
    
    with open(task.ruined_image.path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
        
    pmpt = (f"PROTOCOL v2.1 (INSTANCE: 4_{int(time.time())}): FRESH SCAN HANDSHAKE. "
            f"ACT AS A SENIOR FORENSIC ARCHAEOLOGIST. NO PREVIOUS MEMORY. "
            f"ANALYZE THIS SPECIFIC IMAGE AT THIS INSTANCE. "
            f"INSTRUCTION: ANALYZE PHYSICAL TEXTURES, STRUCTURAL FRACTURES, AND MATERIAL DEPTH. "
            f"Respond ONLY with a RAW JSON object using Double Quotes for all keys and strings. "
            f"Schema: {{ \"detected_object\": \"name\", \"ruined_percentage\": 35, \"report_dossier\": \"text\" }}. ")
            
    headers = {"Authorization": f"Bearer {settings.GEMINI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "meta/llama-3.2-11b-vision-instruct",
        "messages": [{"role": "user", "content": [{"type": "text", "text": pmpt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}],
        "max_tokens": 1200, "temperature": 0.5, "top_p": 1.0
    }
    
    print("Sending request...")
    res = requests.post("https://integrate.api.nvidia.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")

if __name__ == "__main__":
    run()
