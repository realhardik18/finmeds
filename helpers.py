from creds import SERP_API_KEY_1
import requests


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



print(GetPolicy('medanta','gurugram'))