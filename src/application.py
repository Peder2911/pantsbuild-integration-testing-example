from typing import List, Literal
import http
import fastapi
import starlette.responses
import uvicorn
import pydantic
import ast
import sqlite3

db = sqlite3.connect(":memory:",check_same_thread=False)
with db:
    db.execute("create table snippets(id integer primary key, name varchar unique, snippet varchar)")

class SnippetListing(pydantic.BaseModel):
    id: int
    name: str

class SnippetSubmission(pydantic.BaseModel):
    name: str
    snippet: str

class SnippetDetail(SnippetListing, SnippetSubmission):
    ...

class SnippetsListResponse(pydantic.BaseModel):
    snippets: List[SnippetListing]

class StatusMessage(pydantic.BaseModel):
    status: Literal["ok"]

app = fastapi.FastAPI()

@app.get("/status")
def status():
    return StatusMessage(status = "ok")

@app.post("/snippets", response_model = SnippetDetail, status_code = http.HTTPStatus.CREATED)
def create_snippet(snippet: SnippetSubmission):
    try:
        ast.parse(snippet.snippet)
    except SyntaxError:
        return starlette.responses.Response(status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY)
    with db:
        try:
            db.execute("insert into snippets(name,snippet) values(?,?)", (snippet.name, snippet.snippet))
            id,*_ = db.execute("select last_insert_rowid()").fetchone()
        except sqlite3.IntegrityError:
            return starlette.responses.Response(status_code = http.HTTPStatus.CONFLICT) 
    return SnippetDetail(id = id, name = snippet.name, snippet = snippet.snippet )

@app.get("/snippets")
def list_snippets():
    return SnippetsListResponse(snippets = [SnippetListing(id=id,name=name) for id,name in db.execute("select id,name from snippets")])

@app.get("/snippets/{id:str}")
def show_snippet():
    try:
        id,name,snippet = db.execute("select id,name,snippet from snippets").fetchone()
    except TypeError:
        return starlette.responses.Response(status_code = http.HTTPStatus.NOT_FOUND)
    return SnippetDetail(id = id, name = name, snippet = snippet)

@app.delete("/snippets/{id:int}")
def delete_snippet(id: int):
    db.execute("delete from snippets where id=?", (id,))
    return starlette.responses.Response(status_code = http.HTTPStatus.NO_CONTENT)

if __name__ == "__main__":
    uvicorn.run(app, port = 8000, host = "0.0.0.0")
