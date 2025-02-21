import utils.http_session
import utils.transport
import utils.session
from flask import Flask, request, url_for
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

# Twilio credentials (replace with your own)
TWILIO_SID = "AC51efcfc1636ff0938e2bb457344d72b6"
TWILIO_AUTH_TOKEN = "1fbd597af8b8308ac9fecbc117d61d2b"
TWILIO_PHONE_NUMBER = "+18633410360"  # Your Twilio phone number

# Create a Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


@app.route("/",methods=["GET"])
def home_route():
    return f"Welcome!"



@app.route("/call", methods=["GET"])
def make_call():
    # The number you want to call
    to_number = "+923456332300"  # Replace with the recipient's phone number

    # The URL for the TwiML instructions to execute when the call is answered
    twiml_url = url_for('twiml', _external=True)
    

    # Make the outbound call
    call = client.calls.create(
        to=to_number,
        from_=TWILIO_PHONE_NUMBER,
        url=twiml_url
    )

    return f"Call initiated to {to_number}"

@app.route("/twiml", methods=["GET", "POST"])
def twiml():
    response = VoiceResponse()

    # Create a Gather to listen for the user input
    gather = Gather(num_digits=1, action=url_for('handle_choice', _external=True))
    gather.say("Hello! Please press 1 for sales, 2 for support, or 3 for more options.")

    response.append(gather)

    # If no input is received, prompt the user again or end the call
    response.say("We didn't receive any input. Goodbye.")
    response.hangup()

    return str(response)


@app.route("/process_input", methods=["POST"])
def process_input():
    # Get the digit pressed by the user
    digit_pressed = request.form['Digits']

    # Handle the input accordingly and trigger API calls
    if digit_pressed == "1":
        # Trigger API for Sales
        return "You pressed 1 for Sales. API for Sales is triggered!"
    elif digit_pressed == "2":
        # Trigger API for Support
        return "You pressed 2 for Support. API for Support is triggered!"
    elif digit_pressed == "3":
        # Trigger API for More Options
        return "You pressed 3 for More Options. API for More Options is triggered!"
    else:
        return "Invalid input. Please try again."

if __name__ == "__main__":
    app.run(debug=True)
