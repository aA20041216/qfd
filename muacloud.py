import requests
try:
    response = requests.get("https://www.skymz.com/#/login", timeout=10)
    print(f"连接状态: {response.status_code}")
except Exception as e:
    print(f"连接失败: {e}")
