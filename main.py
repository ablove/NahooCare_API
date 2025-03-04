from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    print("this from home media")
    return {"message": "this from home media"}  # Added return statement

@app.post("/test/{id}")  # Missing curly braces {id}
def test(id: int):
    print(id, "this the id")
    return {"id": id, "message": "this the id"}  # Added return statement