from app.api import API

api = API()

@api.route("/")
def index(req, res):
    res.media = {'message': f'Hello'}

if __name__ == '__main__':
    api.run(host="127.0.0.1", port=5050)