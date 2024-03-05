from flask import  jsonify
import json
from io import BufferedReader
import requests
import base64
from file_namer import FileNamer, FakeFileNamer
from format_error import format_error

def extract_recipe_text(image_file: BufferedReader, fake_extraction: bool) -> str:
    if fake_extraction:
        with open("fake_extract_recipe_respones.txt","r") as response_file:
            return  response_file.read()
    
    im_b64 = base64.b64encode(image_file.read()).decode('utf-8')
    # The api authorization key
    with open("/home/pi/chat_gpt_api_key.txt") as f:
        api_key = f.read()
    # The prompt sent along with the image descriping how chat GPT should respond
    with open('prompt.txt','r') as f:
        # TODO: Uppdate prompt with categories, tags, and better described fields
        prompt = f.read()

    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer %s"%(api_key)
    }

    payload = {
    # using the 4 vision model for image processing
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": "data:image/jpeg;base64,%s"%(im_b64)
            }
            }
        ]
        }
    ],
    # TODO: May want to put this in the advanced options
    # If reponses are getting cutoff, this may need to increase
    "max_tokens": 1200
    }
    response = json.dumps(requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json())
    return response


def process_image_request(image_file, fake_extraction):
    if image_file.filename == '':
        return jsonify({'error_message': 'No image selected'})
    try:
        chat_response = extract_recipe_text(image_file, fake_extraction)

        recipe= json.loads(chat_response)["choices"][0]["message"]["content"]
        recipe = recipe[recipe.find("{"):recipe.rfind("}")+1]
        file_namer = FakeFileNamer() if fake_extraction else FileNamer(json.loads(recipe).get("name"))

        image_file.save(file_namer.file_path(dir='static/recipe_images',extension='.png'))

        return jsonify({'message': 'Image processed successfully', 'recipe': recipe, 'recipe_link':'http://fishpoopsoup.com'})
        
    except Exception as e:
        return jsonify({'error_message': '%s'%(format_error(e))})