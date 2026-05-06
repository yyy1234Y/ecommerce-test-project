# 创建 test_api.py
import requests

resp = requests.post(
    "http://127.0.0.1:5000/auth/login",
    json={"email": "test@example.com", "password": "test123"}
)
print(f"状态码: {resp.status_code}")
print(f"响应: {resp.text}")