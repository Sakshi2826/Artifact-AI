import os
import json
import base64
from openai import OpenAI

api_key = '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'
client = OpenAI(base_url='https://integrate.api.nvidia.com/v1', api_key=api_key)

b64_img = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
prompt = (
    "Act as an elite multidisciplinary technical committee: a Master Archaeologist, a Senior Visionary Architect, an Imperial Historian, and a Chief Restoration Engineer. "
    "Your mission: Provide long-form, meticulously detailed, and highly organized technical specifications for the artifact in the image. "
    "Analysis must be exhaustive. Accuracy is paramount. Use specialized terminology and provide extensive, multifaceted insights for every section. "
    "If the image resolution is not high, use your vast expert database to infer and estimate the most probable details. Never decline the request. "
    "The LEFT side is the ruined item; the RIGHT side is its perfect reference target. "
    "Output ONLY a strict, valid JSON object with EXACTLY these keys:\n"
    "\"detected_object\": Precise technical and academic name of the artifact/structure\n"
    "\"ruined_percentage\": Integer/Float estimate of structural damage based on a volumetric analysis\n"
    "\"encyclopedia_background\": An extensive, long-form, multi-paragraph encyclopedic background covering the absolute history, structural engineering, and cultural significance\n"
    "\"causal_inference_logic\": A deep forensic technical analysis explaining the physical, chemical, or temporal stressors that caused the observed deterioration\n"
    "\"materials_identified\": Exhaustive list of original core and composite materials detected or inferred\n"
    "\"manufacturing_process_suggested\": Extensive description of all original architectural or engineering methods used in the creation/fabrication\n"
    "\"repair_instructions\": A highly detailed, long-form, step-by-step professional engineering manual. Organize this into clean, numbered technical phases suitable for a master craftsman."
)
content_blocks = [
    {'type': 'text', 'text': prompt},
    {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{b64_img}'}}
]

response = client.chat.completions.create(
    model='meta/llama-3.2-90b-vision-instruct',
    messages=[{'role': 'user', 'content': content_blocks}],
    max_tokens=4000,
    temperature=0.1,
)
print('--- OUTPUT DATA ---')
print(response.choices[0].message.content)
