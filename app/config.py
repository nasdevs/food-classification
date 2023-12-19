class Config:
    confidence_standard = 0.6

    model_path = 'model/food-classification-model.h5'
    nutrition_path = 'data/nutrition.csv'

    upload_folder = 'static/uploads/'
    allowed_extension = set(['png', 'jpg', 'jpeg'])