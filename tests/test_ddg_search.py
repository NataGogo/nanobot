import json
from ddgs import DDGS

def get_ddg_results(keywords, max_results=5):
    results_list = []
    
    # 使用 DDGS 迭代器获取搜索结果
    with DDGS() as ddgs:
        # keywords: 搜索词
        # region: 地区代码 (wt-wt 是全球, cn-zh 是中国)
        # safesearch: 安全搜索级别 (on, moderate, off)
        # timelimit: 时间限制 (d-天, w-周, m-月, y-年)
        ddgs_gen = ddgs.text(
            keywords, 
            region="wt-wt", 
            safesearch="moderate", 
            timelimit=None, 
            max_results=max_results
        )
        
        for r in ddgs_gen:
            results_list.append(r)
            
    # 返回原始列表而不是 JSON 字符串，这样调用者可以直接遍历
    return results_list

# 测试调用
query = "AI agent 开源项目排名"
results = get_ddg_results(query)

# 解析DuckDuckGo返回结果
# 在 get_ddg_results 改为返回列表之后, 这里的 results 直接就是一个可迭代的 list
if not results:
    print(f"No results for: {query}")
else:
    # print(f"duckduckgo returned: {results}")
    lines = [f"Results for: {query}\n"]
    # 遍历列表中的字典项
    for i, item in enumerate(results):
        # item 本身是一个 dict, 可通过 key 访问 title, href, body 等字段
        lines.append(f"{i}. {item.get('title','')}\n   {item.get('href','')}")
        if desc := item.get("body"):
            lines.append(f"   {desc}")
    print("\n".join(lines))
