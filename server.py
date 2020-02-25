from flask import Flask, url_for, request, Response
# import src.capsule_net as capsule_net
import json
import base64
import os

app = Flask(__name__)


@app.route('/', methods=['POST'])
def api_root():
    return 'Welcome'


@app.route('/prediction', methods=['POST'])
def api_prediction():
    #     print(request.headers['Authorization'])
    print(request.json['image'])
    image_path = 'images/'
    if os.path.isdir(image_path) is False:
        os.mkdir(image_path, 0o777)

    with open(image_path + "foo.png", "wb") as f:
        f.write(base64.b64decode(str(request.json['image'])))

    js = json.dumps({
        'disease': 'Early Blight',
        'accuracy': 92,
        'success': True
    })
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid


if __name__ == '__main__':
    app.run()
