from flask import Flask, render_template, request
from helpers import GetPolicy
import json

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

if __name__ == '__main__':
    app.run(debug=True)
