from fastapi import FastAPI
import uvicorn

db = {
    1: {"id": 1, "name": "Johnsmith", "email": "johnsmith@example.com"},
    2: {"id": 2, "name": "MarkSmith", "email": "marksmith@example.com"}
}

api = FastAPI()

@api.get("/users/{user_id}")
def get_profile(user_id: int):
    return db.get(user_id,
                  {"error": "user not found"})


uvicorn.run(api)
#note: this would only return a user if one is stored in the database
#example  http://127.0.0.1:8000/users/2
# result {"id":2,"name":"MarkSmith","email":"marksmith@example.com"}

