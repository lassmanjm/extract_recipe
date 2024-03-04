from flask import Flask, render_template, request, jsonify
from PIL import Image
from extract_recipe_text import extract_recipe
from fake_extract_recipe_text import extract_recipe as fake_extract_recipe
from flask_cors import CORS
import re
import json


app = Flask(__name__)
CORS(app, resources={r"/python_server/*": {"origins": "http://localhost:5000"}})

def process_image_internal(recipe_extraction_method, image_file):
    if image_file.filename == '':
        return jsonify({'message': 'No image selected'}), 400

    try:
        # Process the image using your Python script
        chat_response = recipe_extraction_method(image_file)
        print(chat_response)
        recipe= json.loads(chat_response)["choices"][0]["message"]["content"]
        recipe = recipe[recipe.find("{"):recipe.rfind("}")+1]

        # Send the save path in the response
        return jsonify({'message': 'Image processed successfully', 'recipe': recipe, 'recipe_link':'http://fishpoopsoup.com'})
        
    except Exception as e:
        return jsonify({'message': 'Error processing image: %s'%(str(e))}, 500)

@app.route('/extract_recipe')
def index():
    return render_template('index.html')


@app.route('/extract_recipe/process_image', methods=['POST'])
def process_image():
    print(request.files)
    print(request.form)
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({'error_message': 'Error in request: No image provided.'}), 400

    advanced_options_string = request.form.get('advanced_options')
    if not advanced_options_string:
        return jsonify({'error_message': 'Error in request: advanced_options field not found.'})
    try:
        advanced_options =json.loads(advanced_options_string)
        fake_call = advanced_options["fake_call"]
    except Exception as e:
        return jsonify({'error_message': 'Error in request advanced_options field: %s'%e})
    if fake_call == 'true':
        print(1)
        recipe_extraction_method = fake_extract_recipe
    else:
        print(2)
        recipe_extraction_method = extract_recipe
    return process_image_internal(recipe_extraction_method, image_file)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
