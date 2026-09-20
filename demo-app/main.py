from fastapi import FastAPI

app = FastAPI()


@app.get("/add") # When a GET call comes at the endpoint /add, then run the function below
def add(a: float, b: float):
    return {"a": a, "b": b, "sum": a + b}
