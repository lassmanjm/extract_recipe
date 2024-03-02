import base64
import json
import requests
from PIL import Image
from io import BufferedReader, BytesIO

# OpenAI API Key


# # Function to encode the image
def encode_image(image_file: BufferedReader):
    return base64.b64encode(image_file.read()).decode('utf-8')

# def create_headers(api_key:str) -> dict:


def extract_recipe(image_file: BufferedReader) -> str:
    im_b64 = encode_image(image_file)
    with open("/home/pi/chat_gpt_api_key.txt") as f:
        api_key = f.read()
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer %s"%(api_key)
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": """can you take the recipe in the photo and produce a JSON with the following fields if they can be found or inferred?
    -name (string)
    -description (string)
    -servings (string)
    -total_time (string in the format "{{minutes}}M{{hours}}H")
    -ingredients (array of strings)
    -steps (array of strings)

    note: total _time is the summation of cooking time and prep time if it is not mentioned directly. Print only the JSON itself, no other text. The first character you return should be the opening '{' of the json and the last should be the closing '}' of the json. 
    """
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
    "max_tokens": 1200
    }

    response = json.dumps(requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json())
    return response

    
# image = Image.open("image.jpg")
# # image.save('/home/pi/tmp_images/test.jpg')
# with open("image.jpg", "rb") as image:
#     print(extract_recipe(image))
