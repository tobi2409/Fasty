@app.get("/!!path!!/{name}")
def helloWorld(name: str):
    return {"message": "Hello World from Server to " + name}
