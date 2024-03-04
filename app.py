from flask import Flask, render_template, request, jsonify
from PIL import Image
from extract_recipe_text import extract_recipe
from fake_extract_recipe_text import extract_recipe as fake_extract_recipe
from flask_cors import CORS
import re
import json


app = Flask(__name__)
CORS(app, resources={r"/python_server/*": {"origins": "http://localhost:5000"}})

def process(extract_recipe):
    if 'image' not in request.files:
        return jsonify({'message': 'No image provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'message': 'No image selected'}), 400

    try:
        # Process the image using your Python script
        chat_response = extract_recipe(image_file)
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
    return process(extract_recipe)

@app.route('/extract_recipe/fake_process_image', methods=['POST'])
def fake_process_image():
    return process(fake_extract_recipe)

@app.route('/extract_recipe/process_recipe', methods=['POST'])
def process_recipe():
    recipe=request.form.to_dict()
    # print("name: ", recipe["name"])
    # ingredients = {key:value for (key,value) in recipe.items() if key.startswith('ingredient')}
    # print( "ingredients:")
    # for 
    for key,value in recipe.items():
        print(key, ": " , value)
    return jsonify({'link':'google.com'})




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
