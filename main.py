# This is a sample Python script.
import os

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import time
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# OpenAI API key setup
openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

# Function to submit the initial POST request
def submit_form_analysis(url, headers, data):
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 202:
        operation_location = response.headers['Operation-Location']
        print(f"Operation Location: {operation_location}")
        return operation_location
    else:
        print(f"Error: {response.status_code}")
        print(f"Message: {response.text}")
        return None

# Function to poll the operation status using the GET request
def poll_operation_status(operation_location, headers):
    while True:
        response = requests.get(operation_location, headers=headers)
        if response.status_code == 200:
            result = response.json()
            status = result.get("status")
            if status in ["succeeded", "failed"]:
                return result
            else:
                print(f"Operation status: {status}, retrying in 1 second...")
                time.sleep(1)  # Wait for 1 second before retrying
        else:
            print(f"Error: {response.status_code}")
            print(f"Message: {response.text}")
            return None

def generate_prompt_from_data(data):
    # Construct a prompt based on the extracted data
    # This function needs to be tailored based on how the data is structured and what you want to generate with it
    # For simplicity, let's assume we want to summarize the extracted text
    prompt = f"Summarize this text:\n\n{data}"
    return prompt

def ask_openai_to_generate_text(prompt):
    system_prompt = {"role": "system",
                         "content": "Your job is to take Unstructured data and extract patient details and medicines prescribed and doctor details. The unstructured data is the text extracted from a image of a dummy prescription. "}

    messages = []
    messages.append(system_prompt)
    user_prompt = {"role": "user", "content": prompt}
    messages.append(user_prompt)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print(response)
    return response.choices[0].message.content

# Press the green button in the gutter to run the script.
def ocr(url):
    # Initial POST request setup
    subscription_key = os.getenv('AZURE_AI_SUBSCRIPTION_KEY')
    image_url = 'https://github.com/emarco177/ice_breaker/assets/131140093/9cf515ec-d9bc-44bd-a910-449612a6a95e'
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key
    }
    data = json.dumps({"urlSource": image_url})

    # Submit the initial request and get the operation location
    operation_location = submit_form_analysis(url, headers, data)

    # Poll the operation status if we received an operation location URL
    if operation_location:
        result = poll_operation_status(operation_location, headers)
        if result:
            print("Operation completed.")

            pretty_json = json.dumps(result, indent=4)
            extracted_text = result.get('analyzeResult').get('content')

            prompt = generate_prompt_from_data(extracted_text)

            # Use OpenAI API to generate text based on the prompt
            generated_text = ask_openai_to_generate_text(prompt)

            print("Generated Text:")
            return(generated_text)
        else:
            return("Failed to retrieve the result.")