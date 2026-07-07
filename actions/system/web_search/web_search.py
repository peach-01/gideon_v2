class WebSearchTool:

    name = "web_search"

    async def search(self, query: str):
        return {
            "query": query,
            "results": []
        }