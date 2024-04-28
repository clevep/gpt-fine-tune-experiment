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
DEFAULT_FILE_PATH = os.path.join(current_directory, "fine_tune_data.jsonl")

openai_client = openai.OpenAI()


def upload_file(file_path=DEFAULT_FILE_PATH):
    ## Make the API request
    response = openai_client.files.create(
        file=open(file_path, "rb"),
        purpose="fine-tune"
    )
    return response.id


def create_fine_tune_job(file_id):
    response = openai_client.fine_tuning.jobs.create(
        training_file=file_id,
        model=MODEL
    )
    print(response)


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