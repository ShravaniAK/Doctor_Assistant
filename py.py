import requests
from flask import Flask, request, jsonify
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

@app.route('/predict', methods=['GET'])
def predict():
    symptoms = request.json.get('symptoms', [])
    print(symptoms)
    result_df = test_input(symptoms)
    specialist = result_df['Specialist'].iloc[0]  # Assuming there's only one specialist predicted
    return jsonify({'Specialist': specialist})

# Main code
print("Enter your symptoms (comma-separated):")
symptoms = input().split(',')

specialties = get_specialty_from_api(symptoms)
print("Specialties fetched from API:")
for specialty in specialties:
    print(f"Disease: {specialty['Disease']}, Specialist: {specialty['Specialist']}, Chances: {specialty['Chances']}%")

# Find the specialist with the highest chance
specialist_with_highest_chance = max(specialties, key=lambda x: x['Chances'])['Specialist']

print(f"\nSpecialist with the highest chance: {specialist_with_highest_chance}")

print("Enter the day of the week (e.g., Monday, Tuesday, etc.):")
day = input().capitalize()  # Capitalize the first letter to match the day format in the database

doctors = find_doctors(specialist_with_highest_chance, day)
if doctors:
    print(f"Found {len(doctors)} doctors with specialty '{specialist_with_highest_chance}' available on {day}:")
    for doctor in doctors:
        print(f"{doctor['name']} ({doctor['time']}), Rating: {doctor['rating']}")
else:
    print(f"No doctors found with specialty '{specialist_with_highest_chance}' available on {day}.")

if __name__ == '__main__':
    app.run(debug=True)
