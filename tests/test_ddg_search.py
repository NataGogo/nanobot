import json
from duckduckgo_search import DDGS

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
            
    # 将列表转换为格式化的 JSON 字符串
    return json.dumps(results_list, indent=4, ensure_ascii=False)

# 测试调用
query = "Python 异步编程"
json_output = get_ddg_results(query)

print(f"搜索词: {query}")
print(json_output)