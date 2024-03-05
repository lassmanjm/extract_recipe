from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from process_image_request import process_image_request
import json
from format_error import format_error


app = Flask(__name__, static_url_path='/extract_recipe/static')
CORS(app, resources={r"/python_server/*": {"origins": "http://localhost:5000"}})


@app.route('/extract_recipe')
def index():
    return render_template('index.html')


@app.route('/extract_recipe/process_image', methods=['POST'])
def process_image():
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
        return jsonify({'error_message':format_error(e)})
    return process_image_request(image_file, fake_call=='true')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
