from io import BufferedReader

def extract_recipe(image_file: BufferedReader) -> str:
    with open("fake_extract_recipe_respones.txt","r") as response_file:
        return  response_file.read()

extract_recipe(None)
