from app.api import API

api = API()


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