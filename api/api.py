from fastapi import FastAPI
from server.WBfinder import finder_cards

app = FastAPI(title='API, version 1.0')

@app.get('/search')
async def search_items(query: str, pages: int = 1):
    results = await finder_cards(search=query, page=str(pages))
    return {"query": query, "pages_searched": pages, "results": results}