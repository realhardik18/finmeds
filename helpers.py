from creds import SERP_API_KEY_1
import requests
from io import BytesIO
import pdfplumber
import replicate
from creds import REPLICATE_API_TOKEN4
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

def GPTQuestions(question):
    client = replicate.Client(api_token=REPLICATE_API_TOKEN4)                

    # Prepare the input dictionary
    input={
        "top_k": 0,
        "top_p": 0.9,
        "prompt": "ONM - (Intra Operative Neuro Monitoring)\n",
        "max_tokens": 512,
        "min_tokens": 0,
        "temperature": 0.6,
        "system_prompt": "You are a medical policy reader expert. your friend has a doubt from the following string. help him out in 60 words. the string could be a keyword or an extract from the policy",
        "length_penalty": 1,
        "stop_sequences": "<|end_of_text|>,<|eot_id|>",
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a medical policy reader expert. your friend has a doubt from the following string. help him out in 60 words. the string could be a keyword or an extract from the policy<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "presence_penalty": 1.15,
        "log_performance_metrics": False
    } 
    for event in client.stream(
        "meta/meta-llama-3-70b-instruct",
        input=input
    ):
        print(str(event), end="")
    

#print(len(read_data()))
GPTQuestions('we')
#print(GetPolicy("tata aig medicare"))