import os
import json
import base64
from openai import OpenAI

# The key you provided from settings.py
api_key = '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'
client = OpenAI(base_url='https://integrate.api.nvidia.com/v1', api_key=api_key)

# A simple 1x1 jpeg to avoid large payloads while testing
b64_img = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
prompt = (
    "Adopt the expert multidisciplinary perspectives of a world-class Archaeologist, an Architect, a Historian, and a Lead Reverse-Engineer. "
    "First, analyze the provided image with extreme accuracy to intelligently recognize exactly what the artifact or structure is. "
    "Output a strict JSON object with EXACTLY the following keys:\n"
    "\"detected_object\": Precise name\n"
    "\"ruined_percentage\": Float\n"
    "\"encyclopedia_background\": Highly intelligent analysis\n"
    "\"causal_inference_logic\": Expert forensic explanation\n"
    "\"materials_identified\": list of strings\n"
    "\"manufacturing_process_suggested\": list of strings\n"
    "\"repair_instructions\": Highly specialized, explicit engineering instructions."
)

content_blocks = [
    {'type': 'text', 'text': prompt},
    {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{b64_img}'}}
]

try:
    response = client.chat.completions.create(
        model='meta/llama-3.2-90b-vision-instruct',
        messages=[{'role': 'user', 'content': content_blocks}],
        max_tokens=4000,
        temperature=0.2,
    )
    print('--- RAW OUTPUT START ---')
    print(response.choices[0].message.content)
    print('--- RAW OUTPUT END ---')
except Exception as e:
    print('ERROR:', e)
