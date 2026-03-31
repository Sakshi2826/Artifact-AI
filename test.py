import urllib.request
import urllib.parse
import json
import uuid

url = 'http://127.0.0.1:8000/api/analyze/'
boundary = uuid.uuid4().hex
headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}

data = f"""--{boundary}
Content-Disposition: form-data; name="image"; filename="test.png"
Content-Type: image/png

fake_image_data_here
--{boundary}--
""".replace('\n', '\r\n').encode('utf-8')

req = urllib.request.Request(url, data=data, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        print("Success:")
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print('HTTP Error:', e.code)
    print(e.read().decode())
