from app.api import API
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"])
]

api = API(middleware=middleware)


data = [
        {'id': 1, 'name': 'Durval Maia', 'age': 19},
        {'id': 2, 'name': 'Davi Dantas', 'age': 9},
        {'id': 3, 'name': 'Rafael Nadal', 'age': 35}
    ]

@api.route("/users")
def get_users():
    return data

@api.route("/user/{user_id:d}")
def get_user(user_id):
    for user in data:
        if user['id'] == user_id:
            result = user

    return result

if __name__ == '__main__':
    api.run(host="127.0.0.1", port=5050)