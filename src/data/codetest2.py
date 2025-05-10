import requests

url = "https://data360.worldbank.org/api/Search/post_data360_search"
headers = {
    "Content-Type": "application/json"
}

payload = {
    "query": "IPC_IPC_P3PLUS",  # 指标 ID
    "lang": "en"
}

response = requests.post(url, json=payload, headers=headers)

try:
    data = response.json()
    print(data)
except ValueError:
    print("响应不是有效的 JSON：")
    print(response.text)
