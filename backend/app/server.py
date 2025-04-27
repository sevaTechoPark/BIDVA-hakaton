import uvicorn
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from semantic_search import SemanticSearch
from fastapi.middleware.cors import CORSMiddleware

search_model = SemanticSearch()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/search')
def search(iPost_data = Body()):
    print(iPost_data)
    document = iPost_data['document']
    word = iPost_data['word']

    search_result = search_model.search(document, word)
    return JSONResponse(search_result)

if __name__ == '__main__':
    uvicorn.run('server:app', host='127.0.0.1', port=5151)