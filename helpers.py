from creds import SERP_API_KEY_1
import requests
from io import BytesIO
import pdfplumber
from llama_cpp import Llama

def GetPolicy(hospital_name,area):            
    hospital_name=hospital_name.replace(' ','+')
    area=area.replace(' ','+')
    params = {
    "api_key": SERP_API_KEY_1,
    "engine": "google",
    "q": f"{hospital_name}+hospital+{area}+policy+filetype%3Apdf",
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

#print(GetPolicy('narayna hospital','hsr layout sector 2'))
print(GetTextFromPolicy('https://narayanahealth.insurance/wp-content/uploads/2024/06/Narayana-Aditi-Prospectus.pdf'))