from flask import Flask, render_template, request
from helpers import GetPolicy,GetTextFromPolicy,get_llm_output
import json
import requests
import requests
import pdfplumber
from io import BytesIO
import re
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hospitals')
def hospitals():
    return render_template('hospitals.html')

@app.route('/results', methods=['POST'])
def results():
    # Get the form data
    hospital_name = request.form['hospital']
    state = request.form['state']
    policy_pdf_link=GetPolicy(hospital_name=hospital_name,city=state)
    print(policy_pdf_link)

    # Pass the data to the results page
    return render_template('results.html', hospital=hospital_name, state=state,link=policy_pdf_link)

@app.route('/NGO')
def ngo():
    with open('data.json','r',encoding='utf-8') as file:
        data=json.load(file)
    return render_template('ngo.html',data=data)

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/about-us')
def about():
    return render_template('about-us.html')

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

@app.route('/get_pdf_page_text')
def get_pdf_page_text():
    page = int(request.args.get('page'))
    link = request.args.get('link')
    
    # Call the function to get the text for the specified page from the link
    page_text = GetTextFromPolicy(link, page)
    summarized=get_llm_output(page_text)    
    return summarized

if __name__ == '__main__':
    app.run(debug=True)

