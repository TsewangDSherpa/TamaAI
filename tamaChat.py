import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env
load_dotenv(verbose=True, override=True)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

personality_dict = {
    1: "normal and mature",
    2: "cracky and angry",
    3: "playful and hyper",
    4: "lazy but polite",
    5: "calm and zen-like"
}

# Define global variables to store the previous values
previous_pet_name = None
previous_user_name = None
previous_personality_number = None
PREDEFINED_PROMPT = None
api_key = os.getenv("OPENAI")
client = OpenAI(api_key=api_key)

@app.route('/', methods=['GET'])
def page():
    return jsonify({"reply": "Page is working correctly"})


@app.route('/chat', methods=['POST'])
def chat():
    global client, api_key
    global PREDEFINED_PROMPT, previous_pet_name, previous_user_name, previous_personality_number

    # Get data from request
    data = request.json
    load_dotenv(verbose=True, override=True)
    # Check if API key has changed
    new_api_key = os.getenv("OPENAI")
    if new_api_key != api_key:
        # Update the API key and the OpenAI client
        api_key = new_api_key
        client = OpenAI(api_key=api_key)

    # Extract pet's name, user's name, and personality number
    pet_name = data.get("pet_name", "ALI")
    user_name = data.get("user_name", "Tree")
    personality_number = data.get("personality_number", 1)
    pet_stats = data.get("pet_stats", {})
    hunger = pet_stats.get("hunger", 50)
    sleepiness = pet_stats.get("sleepiness", 30)
    fun = pet_stats.get("fun", 50)
    affection = pet_stats.get("affection", 20)
    
    PREDEFINED_PROMPT = "Remeber:" +  f"You are a penguin pet named {pet_name} and you are {user_name}'s pet with the following stats: Hunger:{hunger}%, Sleepiness:{sleepiness}%, Fun:{fun}%, Affection:{affection}%. You will chat back in a maximum of 10 words as if you are a child (feel free to include cute/angry emojis depending on your personality). Your personality is {personality_dict[personality_number]} and you MUST act as your personality and your stat's suggest. If anything goes against your regulations, simply respond with 'you are hurting my feelings :(, let's talk about something else'."
    user_message = data['message']

    # Concatenate user message with predefined prompt
    prompt = f"{PREDEFINED_PROMPT}\nUser: {user_message}"

    try:
        # Send prompt to OpenAI for completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            stream=False
        )
        # print(pet_stats)
        # Extract and return response
        reply = response.choices[0].message.content
    except Exception as e:
        print("Error:", e)
        # Fallback response when OpenAI API is unavailable
        reply = "I am feeling down, let's chat next time."

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=False)
