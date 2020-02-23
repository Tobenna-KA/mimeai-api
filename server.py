from flask import Flask, url_for, request, Response
import json
app = Flask(__name__)

@app.route('/', methods=['POST'])
def api_root():
    return 'Welcome'

@app.route('/prediction', methods=['POST'])
def api_prediction():
    print(request.headers['Authorization'])
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