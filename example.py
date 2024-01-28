import json
from starlette.responses import JSONResponse
from app.api import API

api = API()

@api.route("/")
def get_users():
    data = [
        {'id': 1, 'name': 'Durval Maia', 'age': 19},
        {'id': 2, 'name': 'Davi Dantas', 'age': 9},
        {'id': 3, 'name': 'Rafael Nadal', 'age': 35}
    ]

    json_data = json.dumps({'data': data})
    return json_data

@api.route("/oi")
def oi():
    return {'message': 'oi'}

if __name__ == '__main__':
    api.run(host="127.0.0.1", port=5050)