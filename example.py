from app.api import Api
from app.middleware import Middleware
from app.middleware import CORSMiddleware
from app.staticfiles import StaticFiles

middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"])
]

api = Api(middleware=middleware)
api.mount(path="/static", app=StaticFiles(directory="static"), name="static")

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