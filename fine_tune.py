import dotenv
import openai
import os
import requests

dotenv.load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo-0613')

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Join the directory with the new filename
DEFAULT_FILE_PATH = os.path.join(current_directory, "fine_tune_data.json")

openai_client = openai.OpenAI()


def upload_file(file_path=DEFAULT_FILE_PATH):
    # Set the request headers and data
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "purpose": "fine-tune"
    }
    files = {
        "file": open(file_path, "rb")
    }
    # Make the API request
    response = requests.post("https://api.openai.com/v1/files", headers=headers, data=data, files=files)
    return response.json()['id']


def create_fine_tune_job(file_id):
    # Set the request headers and data
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    data = {
        "training_file": file_id,
        "model": MODEL,
    }

    # Make the API request
    response = requests.post("https://api.openai.com/v1/fine_tuning/jobs", headers=headers, json=data)
    print(response.json())


def query_fine_tune_model(fine_tune_model_name, system_prompt=None, user_prompt=None):
    if system_prompt is None:
        messages = []
    else:
        messages = [
           {"role": "system", "content": system_prompt},
        ]

    if user_prompt is None:
        user_prompt = input('Enter a prompt:\n')

    messages.append(
        {"role": "user", "content": user_prompt}
    )

    # Make an API call to the OpenAI GPT model
    response = openai_client.chat.completions.create(
        model=fine_tune_model_name,
        messages=messages
    )

    # Print the response text
    print(response)