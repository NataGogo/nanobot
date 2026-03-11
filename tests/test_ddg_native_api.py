import requests
import json

def get_official_instant_answer(query):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # 直接返回 JSON 结果
        return response.json()
    else:
        return {"error": "请求失败"}

# 示例：搜索 "Python"
official_result = get_official_instant_answer("2026年AI Agent最新发展趋势")
print(json.dumps(official_result, indent=4))