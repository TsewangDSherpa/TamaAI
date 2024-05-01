import requests

# URL of the Flask server
# SERVER_URL = "https://tama-ai.vercel.app/chat"
SERVER_URL = "http://127.0.0.1:5000/chat"

# Message to send
user_message = "You hungry"

# Define pet's name, user's name, and personality number
pet_name = "AaLI"
user_name = "Ai"
personality_number = 1

# JSON payload
payload = {
    "pet_name": pet_name,
    "user_name": user_name,
    "personality_number": personality_number,
    "message": user_message,
    "pet_stats":{"hunger":80, "sleepiness":10, "fun":100, "affection":10}
}

# Send POST request to the server
response = requests.post(SERVER_URL, json=payload)

# Check if request was successful
if response.status_code == 200:
    # Print AI-generated reply
    print("AI reply:", response.json()["reply"])
else:
    print("Error:", response.text)
