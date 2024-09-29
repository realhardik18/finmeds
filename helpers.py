from creds import SERP_API_KEY_1
import requests
from io import BytesIO
import pdfplumber
import replicate
from creds import REPLICATE_API_TOKEN3
import re

def GetPolicy(name_of_company):                    
    params = {
    "api_key": SERP_API_KEY_1,
    "engine": "google",
    "q": f"health+insurance+policy+{name_of_company}+filetype%3Apdf",
    "location": "India",
    }    
    URL=f"https://serpapi.com/search.json?engine=google&q={params['q']}&location={params['location']}&google_domain=google.com&gl=us&hl=en&api_key={params['api_key']}"
    response=requests.get(URL).json()
    return response['organic_results'][0]['link']

#https://narayanahealth.insurance/wp-content/uploads/2024/06/Narayana-Aditi-Prospectus.pdf
def GetTextFromPolicy(link_to_policy):
    text_corpus=''
    response=requests.get(link_to_policy)
    with BytesIO(response.content) as policy:
        with pdfplumber.open(policy) as pdf:
            for page in pdf.pages:
                text=page.extract_text()
                text_corpus+=text
    with open('text.txt','w+') as file:
        file.write(text_corpus)
    return text_corpus

def read_data():
    with open("text.txt",'r') as file:
        data=file.read().strip()
    clean_data = re.sub(r'[^a-zA-Z0-9\s]', '', data)
    if len(clean_data)>32000:
        return clean_data[0:32000]
    else:
        return clean_data

def GPTQuestions():
    client = replicate.Client(api_token=REPLICATE_API_TOKEN3)            
    context_info = str(read_data())

    prompt = "i am 75M from a very wealthy family suggest me 3 health plans from the context and my per month approx investments. tell me the name of the plans too"

    # Prepare the input dictionary
    input = {
        "top_p": 0.9,
        "prompt": prompt,
        "min_tokens": 0,
        "temperature": 0.6,
        "prompt_template": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant.\n\n'{context_info}'\n\n<|start_header_id|>user<|end_header_id|>\n\n{{prompt}}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "presence_penalty": 1.15
    }    
    for event in client.stream(
        "meta/meta-llama-3-70b-instruct",
        input=input
    ):
        print(event, end="")
    

#print(len(read_data()))
#GPTQuestions()
print(GetPolicy("tata aig medicare"))