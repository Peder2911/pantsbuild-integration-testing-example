import fastapi
import uvicorn
import pydantic

class HelloWorldResponse(pydantic.BaseModel):
    message: str

app = fastapi.FastAPI()

@app.get("/")
def hello_world():
    return HelloWorldResponse(message = "Hello world!") 

if __name__ == "__main__":
    uvicorn.run(app, port = 8000, host = "0.0.0.0")

