from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 5) -> str:
    """
    Performs a web search using DuckDuckGo and returns formatted results.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n")
        
        if not results:
            return "검색 결과가 없습니다."
            
        return "\n---\n".join(results)
    except Exception as e:
        return f"웹 서치 중 오류 발생: {str(e)}"
