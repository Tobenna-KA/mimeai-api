import shutil

from http import HTTPStatus
from flask import Blueprint, url_for, request, Response
from flasgger import swag_from
from api.model.welcome import WelcomeModel
from api.schema.welcome import WelcomeSchema
import api.src.capsule_net as capsule_net
import api.src.pipeline as pipeline
import json
import base64
import os
import datetime

home_api = Blueprint('api', __name__)


@home_api.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Welcome to the Flask Starter Kit',
            'schema': WelcomeSchema
        }
    }
})
def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = WelcomeModel()
    return WelcomeSchema().dump(result), 200


@home_api.route('/prediction', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Welcome to the Flask Starter Kit',
            'schema': WelcomeSchema
        }
    }
})

def api_prediction():
    #     print(request.headers['Authorization'])
    # print(request.json['image'])
    image_path = 'images/'
    if os.path.isdir(image_path) is False:
        os.mkdir(image_path, 0o777)
    image_path += str(datetime.datetime.now()) + ".jpeg"
    # print(request.json['image'])
    image_base64 = request.json['image']
    if str(request.json['image']).startswith('data:image/jpeg;base64,'):
        image_base64 = image_base64[len('data:image/jpeg;base64,'): len(image_base64)]
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(image_base64))
    print(os.path.dirname(os.path.abspath(__file__)))
    dir_name = os.path.dirname(os.path.abspath(__file__))
    # prediction = capsule_net.capsule_prediction(image_path)
    prediction = pipeline.get_class(image_path)
    # prediction = pipeline.get_class(dir_name + '/003a5321-0430-42dd-a38d-30ac4563f4ba___Com.G_TgS_FL 8121_180deg.jpeg')

    if 'error' in prediction:
        js = json.dumps({
            'disease': 'Error',
            'description': prediction['error'],
            'accuracy': 0,
            'image_path': '',
            'success': True
        })
        resp = Response(js, status=200, mimetype='application/json')
        return resp

    print(os.path)
    if not os.path.isdir('predicted_images'):
        os.mkdir('predicted_images', 0o777)
    if not os.path.isdir('static/predicted_images/' + prediction['disease']):
        os.mkdir('static/predicted_images/' + prediction['disease'])

    # move the file
    shutil.move(image_path, 'static/predicted_images/' + prediction['disease'] + "/" + os.path.basename(image_path))
    descriptions = {
        'Early_blight': {
            'text': 'Common on tomato and potato plants, early blight is caused by the fungus '
                    'Alternaria solani and occurs throughout the United States.'
                    ' Symptoms first appear on the lower, older leaves as small brown spots with'
                    ' concentric rings that form a “bull’s eye” pattern. As the disease matures,'
                    ' it spreads outward on the leaf surface causing it to turn yellow,'
                    ' wither and die. Eventually the stem, fruit and upper '
                    'portion of the plant will become infected. Crops can be severely damaged.',
            'link': 'https://www.planetnatural.com/pest-problem-solver/plant-disease/early-blight/'
        },
        'Late_blight': {
            'text': 'Found on tomato and potato plants, late blight is caused by the fungus Phytophthora '
                    'infestans and is common throughout the United States. True to its name, the disease '
                    'occurs later in the growing season with symptoms often not appearing until after blossom.',
            'link': 'https://www.planetnatural.com/pest-problem-solver/plant-disease/late-blight/'
        },
        'Bacterial_spot': {
            'text': 'Bacterial spot is caused by four species of Xanthomonas and occurs worldwide wherever '
                    'tomatoes are grown. Bacterial spot causes leaf and fruit spots, which leads to'
                    ' defoliation, sun-scalded fruit, and yield loss.',
            'link': 'https://content.ces.ncsu.edu/bacterial-spot-of-pepper-and-tomato'
        },
        'Leaf_Mold': {
            'text': 'Simply put, leaf mold is fully decomposed leaves. Don’t turn up your nose. '
                    'Leaf mold has a rich, earthy scent and a dark, crumbly texture.',
            'link': 'https://www.thespruce.com/how-to-make-and-use-leaf-mold-1401907'
        },
        'mosaic_virus': {
            'text': 'Affecting a wide variety of horticultural and vegetable crops — roses, beans, tobacco,'
                    ' tomatoes, potatoes, cucumbers and peppers — mosaic is a viral diseases found'
                    ' throughout the United States.',
            'link': 'https://www.planetnatural.com/pest-problem-solver/plant-disease/mosaic-virus/'
        },
        'Septoria_leaf_spot': {
            'text': 'Septoria leaf spot is caused by a fungus, Septoria lycopersici. It is one of the most'
                    ' destructive diseases of tomato foliage and is particularly severe in areas where wet,'
                    ' humid weather persists for extended periods.',
            'link': 'https://www.missouribotanicalgarden.org/gardens-gardening/your-garden/help-for-the-home-gardener/advice-tips-resources/pests-and-problems/diseases/fungal-spots/septoria-leaf-spot-of-tomato.aspx'
        },
        'spider_mite': {
            'text': 'Many species of the spider mite (family: Tetranychidae), so common in North America,'
                    ' attack both indoor and outdoor plants. They can be especially destructive in greenhouses.',
            'link': 'https://www.planetnatural.com/pest-problem-solver/houseplant-pests/spider-mite-control/'
        },
        'Target_Spot': {
            'text': 'Also known as early blight, target spot of tomato is a fungal disease that attacks a '
                    'diverse assortment of plants, including papaya, peppers, snap beans, potatoes, '
                    'cantaloupe and squash, as well as passion flower and certain ornamentals.',
            'link': 'https://www.gardeningknowhow.com/edible/vegetables/tomato/target-spot-on-tomatoes.htm'
        },
        'Yellow_Leaf_Curl': {
            'text': 'Tomato leaf curl is a destructive viral disease caused by a virus in the Geminivirus family of plant viruses,'
                    ' tomato yellow leaf curl virus (TYLCV).t is spread by whiteflies and can be found in most areas where tomato'
                    ' is grown, causing significant losses.',
            'link': 'https://www.greenlife.co.ke/tomato-yellow-leaf-curl-virus/'
        }
    }

    js = json.dumps({
        'disease': prediction['disease'],
        'description': descriptions[prediction['disease']],
        'accuracy': 92,
        'image_path': 'static/predicted_images/' + prediction['disease'] + "/" + os.path.basename(image_path),
        'success': True
    })
    resp = Response(js, status=200, mimetype='application/json')
    return resp
    # result = WelcomeModel()
    # return WelcomeSchema().dump(result), 200
