from converter import *

app = Flask(__name__)
api = Api(app)

api.add_resource(convert, '/mp4togif')

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5050)