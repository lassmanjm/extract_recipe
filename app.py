from flask import Flask, render_template, request, jsonify
from PIL import Image
from extract_recipe_text import extract_recipe
# from fake_extract_recipe_text import extract_recipe
from flask_cors import CORS
import re
import json


app = Flask(__name__)
CORS(app, resources={r"/python_server/*": {"origins": "http://localhost:5000"}})


@app.route('/extract_recipe')
def index():
    return render_template('index.html')
# def extract_json_from_response(respone

@app.route('/extract_recipe/<string:recipe_json>')
def recipe(recipe_json):
    return render_template("recipe_template.html", recipe=recipe_json)

@app.route('/extract_recipe/process', methods=['POST'])
def process():
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
        print(recipe)

        # Send the save path in the response
        return jsonify({'message': 'Image processed successfully', 'recipe': recipe})
        
    except Exception as e:
        return jsonify({'message': 'Error processing image: %s'%(str(e))}, 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)