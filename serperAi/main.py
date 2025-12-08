import http.client
import json
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SERPER_API_KEY")
conn = http.client.HTTPSConnection("google.serper.dev")
payload = json.dumps({
  "q": "apple inc"
})
headers = {
  'X-API-KEY': '77f1fdb2e2fe368be134eb0d601aee2e7dc357b5',
  'Content-Type': 'application/json'
}
conn.request("POST", "/search", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))