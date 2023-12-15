import os
import numpy as np
import pandas as pd
from flask import jsonify, request
from werkzeug.utils import secure_filename
from PIL import Image
from app import app
from app.model_loader import load_custom_model
from app.nutrition_loader import load_nutrition_data

os.makedirs('static/uploads/', exist_ok=True)

model_path = 'model/food-classification-model.h5'
nutrition_path = 'data/nutrition.csv'

model = load_custom_model(model_path)
labels, nutrition = load_nutrition_data(nutrition_path)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'static/uploads/'

def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/prediction', methods=['POST'])
def prediction():
    if request.method == 'POST':
        image = request.files['image']
        if image and allowed_file(image.filename):
            # Save input image
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)

            # Pre-processing input  image
            img = Image.open(image_path).convert('RGB')
            img = img.resize((224, 224))
            img_array = np.asarray(img)
            img_array = np.expand_dims(img_array, axis=0)
            normalized_img_array = img_array.astype(np.float32) / 127.5 - 1
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_img_array

            # Predicting the image
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = labels[index]
            confidence_score = prediction[0][index]
            nutrition_data = nutrition[index].astype('str')

            return jsonify({
                'status': {
                    'code': 200,
                    'message': 'Success predicting'
                },
                'data': {
                    'category': class_name,
                    'confidence': float(confidence_score),
                    'nutrition': {
                        'energi__kkal': nutrition_data[0],
                        'lemak_total__mg': nutrition_data[1], 
                        'vitamin_A__mg': nutrition_data[2],
                        'vitamin_B1__mg':  nutrition_data[3],
                        'vitamin_B2__mg': nutrition_data[4],
                        'vitamin_B3': nutrition_data[5],
                        'vitamin_C__mg': nutrition_data[6],
                        'karbohidrat_total__mg': nutrition_data[7],
                        'protein__mg': nutrition_data[8],
                        'serat_pangan__mg': nutrition_data[9],
                        'kalsium__mg': nutrition_data[10],
                        'fosfor__mg': nutrition_data[11],
                        'natrium__mg': nutrition_data[12],
                        'kalium__mg': nutrition_data[13],
                        'tembaga__mg': nutrition_data[14],
                        'besi__mg': nutrition_data[15],
                        'seng__mg': nutrition_data[16],
                        'air__mg': nutrition_data[17],
                        'abu__mg': nutrition_data[18]
                    }
                }
            }), 200
        else:
            return jsonify({
                'status': {
                    'code': 400,
                    'message': 'Client side error!'
                },
                'data': None
            }), 400
    else:
        return jsonify({
            'status': {
                'code': 405,
                'message': 'Method not allowed'
            },
            'data': None
        }), 405