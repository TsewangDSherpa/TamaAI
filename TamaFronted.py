import requests

# URL of the Flask server
SERVER_URL = "http://localhost:5000/chat"

# Message to send
user_message = "Lets feed you?"

# Define pet's name, user's name, and personality number
pet_name = "ALI"
user_name = "rt"
personality_number = 1

# JSON payload
payload = {
    "pet_name": pet_name,
    "user_name": user_name,
    "personality_number": personality_number,
    "message": user_message
}

# Send POST request to the server
response = requests.post(SERVER_URL, json=payload)

# Check if request was successful
if response.status_code == 200:
    # Print AI-generated reply
    print("AI reply:", response.json()["reply"])
else:
    print("Error:", response.text)
