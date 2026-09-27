from fastapi import FastAPI

app = FastAPI()

@app.get(
    "/add"
)  # When a GET call comes at the endpoint /add, then run the function below
# Accepting in the form of Query Parameters
def add(a: float, b: float):
    return {"a": a, "b": b, "sum": a + b, "mesaage": "From Query Parameters"}


# Accepting in the form of Path Parameters
@app.get("/add/path/{a}/{b}")
def add(a: float, b: float):
    return {"a": a, "b": b, "sum": a + b, "mesaage": "From Path Parameters"}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}


@app.post("/user")
# Accepting in the form of Request Body
def create_user(user: dict): 
    return {"user_id": user["user_id"], "name": user["name"]}


# Sending info as headers
from fastapi import Request

@app.get("/user/test/headers")
def get_user_headers(request: Request):
    headers_dict = dict(request.headers)
    return {"headers": headers_dict}