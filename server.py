import shutil

from flask import Flask, url_for, request, Response
import src.capsule_net as capsule_net
import json
import base64
import os
import datetime

app = Flask(__name__)


@app.route('/', methods=['POST'])
def api_root():
    return 'Welcome'


@app.route('/prediction', methods=['POST'])
def api_prediction():
    #     print(request.headers['Authorization'])
    # print(request.json['image'])
    image_path = 'images/'
    if os.path.isdir(image_path) is False:
        os.mkdir(image_path, 0o777)
    image_path += str(datetime.datetime.now()) + ".png"
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(str(request.json['image'])))

    prediction = capsule_net.capsule_prediction(image_path)
    if not os.path.isdir('predicted_images'):
        os.mkdir('predicted_images', 0o777)
    if not os.path.isdir('static/predicted_images/' + prediction['disease']):
        os.mkdir('static/predicted_images/' + prediction['disease'])

    # move the file
    shutil.move(image_path, 'static/predicted_images/' + prediction['disease'] + "/" + os.path.basename(image_path))
    js = json.dumps({
        'disease': prediction['disease'],
        'accuracy': 92,
        'image_path': 'static/predicted_images/' + prediction['disease'] + "/" + os.path.basename(image_path),
        'success': True
    })
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/articles/<article_id>')
def api_article(article_id):
    return 'You are reading ' + article_id


if __name__ == '__main__':
    app.run()
