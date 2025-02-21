from flask import Flask, jsonify, request, session, redirect
from functools import wraps
from dotenv import load_dotenv
from flask_cors import CORS
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from utils.chatbot import chat_route
import os
import re 
import uuid

application = Flask(__name__)
CORS(application)  # enable cors

load_dotenv()
API_KEY = os.getenv("API_KEY")

application.secret_key=os.getenv("SECRET_KEY")


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            api_key = request.headers.get("Authorization")
            if not api_key:
                return jsonify({"Error": "Missing API-KEY"}), 400

        except Exception as e:
            return jsonify({"Error": str(e)}), 400
        else:
            if api_key != API_KEY:
                return jsonify({"error": "Invalid API Key"}), 401
            return f(*args, **kwargs)
    return decorated_function

#Pattern matching using re 
def pattern_match(input=""):
    pattern= r'\b(goodbye|bye|byebye|good bye)\b'
    return bool(re.search(pattern, input, re.IGNORECASE))


@application.route('/', methods=['GET'])
@authenticate
def home_route():
    return jsonify({"Message": "Welcome to the channel "})


@application.route("/call", methods=["POST"])
@authenticate
def make_call():
    try:
        data=request.get_json()
        to_call=data.get('to_call')
        from_call=data.get('from_call')
        sid=data.get('sid')
        auth_token=data.get('auth_token')
        if not to_call or not from_call or not sid or not auth_token:
            return jsonify({"Error: Missing Credentials"})
    except Exception as e:
        return jsonify({"Error":str(e)}), 400
    else:

        # Create a Twilio client
        client = Client(sid, auth_token)
        

        # The URL for the TwiML instructions to execute when the call is answered
        #twiml_url = url_for('twiml', _external=True)
        

        #Make the outbound call
        call = client.calls.create(
            to=to_call,
            from_=from_call,
            url="https://dff4-2407-d000-1a-49d1-7c4b-9155-a8f7-2d80.ngrok-free.app/response"
        )
        
        return f"Call initiated to {to_call}"
    
@application.route('/response', methods=["GET", "POST"])
def response():
    response = VoiceResponse()

    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        session["messages"] = []  # Initialize messages list
        session["first_time"] = True  # Mark first-time connection

    if session["first_time"]:
        response.say("Welcome to the channel, you are now connected to the channel.")
        session["messages"].append({"role": "assistant", "content": "Welcome to the channel, you are now connected to the channel."})
        session["first_time"] = False  # Mark that the greeting was sent

    user_input = request.form.get("SpeechResult")
    if user_input:
        check=pattern_match(user_input)
        if check:
            response.hangup()

    if user_input:
        session["messages"].append({"role": "user", "content": user_input})

        # Call chatbot function
        bot_response = chat_route(session["messages"])

        # Append bot response to session
        session["messages"].append({"role": "assistant", "content": bot_response})  

        # Say bot response
        response.say(bot_response)

    # Gather for continued conversation
    gather = response.gather(input="speech", action="https://dff4-2407-d000-1a-49d1-7c4b-9155-a8f7-2d80.ngrok-free.app/response", method="POST", speech_timeout="auto")
    response.append(gather)

    return str(response)

    

    





if __name__ == '__main__':
    application.run(debug=True)
