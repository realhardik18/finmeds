from creds import SERP_API_KEY_1
import requests
from io import BytesIO
import pdfplumber
import requests
from creds import TOGETHER_AI_TOKEN
import json
import re

def GetPolicy(hospital_name,city):
    hospital_name=hospital_name.replace('+','')                    
    city=city.replace('+','')                    
    params = {
    "api_key": SERP_API_KEY_1,
    "engine": "google",
    "q": f"health+insurance+policy+{hospital_name}+{city}+filetype%3Apdf",
    "location": "India",
    }    
    URL=f"https://serpapi.com/search.json?engine=google&q={params['q']}&location={params['location']}&google_domain=google.com&gl=us&hl=en&api_key={params['api_key']}"
    response=requests.get(URL).json()
    return response['organic_results'][0]['link']

#https://narayanahealth.insurance/wp-content/uploads/2024/06/Narayana-Aditi-Prospectus.pdf
def GetTextFromPolicy(link_to_policy, page):
    response = requests.get(link_to_policy)
    with BytesIO(response.content) as policy:
        with pdfplumber.open(policy) as pdf:
            try:
                # Extract text from the specific page
                page_text = pdf.pages[page - 1].extract_text()  # Page numbers are 0-indexed
            except IndexError:
                return "Page number out of range."

    # Clean the extracted text
    clean_data = re.sub(r'[^a-zA-Z0-9\s]', '', page_text)
    
    if len(clean_data) > 32000:
        return clean_data[:32000]
    else:
        return clean_data

def get_llm_output(prompt):
    # Input payload for the API
    input_payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an expert medical policy reader who has to summarize the given text in 100 words."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1"
    }

    # API request
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer TOKEN"
    }

    try:
        response = requests.post('https://api.together.xyz/v1/chat/completions', 
                                 headers=headers, 
                                 data=json.dumps(input_payload))

        if response.status_code != 200:
            # Handle API error
            error_data = response.json()
            print(f"API Error: {error_data}")
            raise Exception(f"HTTP error! status: {response.status_code}, message: {error_data}")

        # Extracting the response content
        data = response.json()
        return data['choices'][0]['message']['content']  # Adjust this according to actual API response structure
    
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred while processing the request: {str(e)}"





   

#print(GetTextFromPolicy('https://narayanahealth.insurance/wp-content/uploads/2024/06/Narayana-Aditi-Prospectus.pdf'))
#print(len(read_data()))
#GPTQuestions('we')
#print(GetPolicy("tata aig medicare delhi"))
#print(GetPolicy('max life','karnataka'))