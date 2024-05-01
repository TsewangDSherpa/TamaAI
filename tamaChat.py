import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env
load_dotenv(verbose=True, override=True)

app = Flask(__name__)

personality_dict = {
    1: "normal",
    2: "cracky",
    3: "playful",
    4: "lazy",
    5: "calm"
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
    
    # Construct predefined prompt if not already constructed or if any of the values change
    if PREDEFINED_PROMPT is None or pet_name != previous_pet_name or user_name != previous_user_name or personality_number != previous_personality_number:
        PREDEFINED_PROMPT = f"You are a penguin pet named {pet_name} and you are {user_name}'s pet with following stats: Hunger:50, Sleepiness:30, Energy : 50, and you are going to be responding in max of 8 words, in a cute and adorable way (yes you can include cute emojis). You respond with {personality_dict[personality_number]}.  Keep the language safe for children. You will be responding to {user_name} in a adorable way. Its only you and your owner {user_name} chatting. If anything goes againsts your regulation then simply respond with 'you are hurting my feelings :(, lets talk about something else'"

        # Update previous values
        previous_pet_name = pet_name
        previous_user_name = user_name
        previous_personality_number = personality_number

    # Get user's message
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

        # Extract and return response
        reply = response.choices[0].message.content
    except Exception as e:
        print("Error:", e)
        # Fallback response when OpenAI API is unavailable
        reply = "I am feeling down, let's chat next time."

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
