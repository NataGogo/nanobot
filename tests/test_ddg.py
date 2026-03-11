import asyncio
import httpx
import json

# 配置常量（和原代码保持一致）
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

async def test_duckduckgo_search(query: str, count: int = 5, proxy: str | None = None):
    """
    测试DuckDuckGo搜索接口调用
    :param query: 搜索关键词
    :param count: 返回结果数量
    :param proxy: 代理地址（可选，如 "http://127.0.0.1:7890"）
    """
    try:
        # 限制结果数量（1-10）
        n = min(max(count, 1), 10)
        
        # 核心调用逻辑（和原代码一致）
        async with httpx.AsyncClient(proxy=proxy) as client:
            r = await client.get(
                "https://duck.co/user/zt",
                params={
                    "q": query,
                    "format": "json",       # 返回JSON格式
                    "no_redirect": 1,       # 不跳转
                    "no_html": 1,           # 过滤HTML
                    "kl": "cn-zh",          # 强制中文结果（适配国内）
                    "skip_disambig": 1      # 跳过歧义页面
                },
                headers={"User-Agent": USER_AGENT},  # 模拟浏览器请求
                timeout=10.0
            )
            r.raise_for_status()  # 触发HTTP错误（如4xx/5xx）

        # 打印原始响应（便于调试）
        print("=== DuckDuckGo 原始响应 ===")
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
        print("\n=== 解析后的搜索结果 ===")

        # 修正原代码的解析逻辑（原代码解析路径错误）
        # 注意：DuckDuckGo的返回结构中没有 "web.results"，正确路径是 "RelatedTopics" 或 "Results"
        results = []
        response_json = r.json()
        
        # 优先解析 RelatedTopics（主要结果）
        if "RelatedTopics" in response_json and isinstance(response_json["RelatedTopics"], list):
            for item in response_json["RelatedTopics"]:
                if isinstance(item, dict) and "FirstURL" in item and item["FirstURL"]:
                    results.append({
                        "title": item.get("Text", "").split(" - ")[0] if "Text" in item else "",
                        "url": item.get("FirstURL", ""),
                        "description": item.get("Text", "").split(" - ")[-1] if " - " in item.get("Text", "") else ""
                    })
        
        # 补充解析 Results（备用结果）
        if not results and "Results" in response_json and isinstance(response_json["Results"], list):
            for item in response_json["Results"]:
                results.append({
                    "title": item.get("Title", ""),
                    "url": item.get("Url", ""),
                    "description": item.get("Description", "")
                })

        # 限制结果数量并展示
        results = results[:n]
        
        if not results:
            print(f"No results for: {query}")
            return

        # 格式化输出结果（和原代码格式一致）
        lines = [f"Results for: {query}\n"]
        for i, item in enumerate(results, 1):
            lines.append(f"{i}. {item.get('title', '')}\n   {item.get('url', '')}")
            if desc := item.get("description"):
                lines.append(f"   {desc}")
        
        print("\n".join(lines))

    except httpx.ProxyError as e:
        print(f"❌ Proxy error: {e}")
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP error (status code {e.response.status_code}): {e}")
    except Exception as e:
        print(f"❌ General error: {e}")
        # 打印异常详情（便于调试）
        import traceback
        traceback.print_exc()

# 测试主函数
if __name__ == "__main__":
    # 配置测试参数
    TEST_QUERY = "2026年AI Agent最新发展趋势"  # 搜索关键词
    TEST_COUNT = 5                              # 返回结果数量
    TEST_PROXY = None                           # 代理地址（如需使用，改为实际地址，如 "http://127.0.0.1:7890"）

    # 运行测试
    print(f"开始测试DuckDuckGo搜索：{TEST_QUERY}")
    print("-" * 50)
    asyncio.run(test_duckduckgo_search(TEST_QUERY, TEST_COUNT, TEST_PROXY))