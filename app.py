from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
connection_string = "mongodb+srv://user:user@cluster0.4hbh3ro.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)
db = client.test
collection = db.specialists

# Function to input symptoms and get the predicted specialist
def get_specialty_from_api(symptoms):
    api_url = "http://127.0.0.1:5000/predict"
    response = requests.get(api_url, json={"symptoms": symptoms})
    if response.status_code == 200:
        data = response.json()
        return data

# Function to find doctors with the specified specialty on the inputted day
def find_doctors(specialty, day):
    query = {"Specialist": specialty, "day": day}
    doctors = collection.find(query)
    return list(doctors)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symptoms = request.form['symptoms'].split(',')
        specialties = get_specialty_from_api(symptoms)
        specialist_with_highest_chance = max(specialties, key=lambda x: x['Chances'])['Specialist']
        day = request.form['day'].capitalize()
        doctors = find_doctors(specialist_with_highest_chance, day)
        if doctors:
            doctors_list = []
            for doctor in doctors:
                doctors_list.append(f"{doctor['name']} ({doctor['time']}), Rating: {doctor['rating']}")
            return render_template('result.html', specialists=specialties, highest_specialist=specialist_with_highest_chance, doctors=doctors_list)
        else:
            return "No doctors found with the specified specialty on the inputted day."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change the port to 5001 or any other available port
