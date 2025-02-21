from flask import Flask, session, request, jsonify
import uuid

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for session management

@app.route("/start", methods=["GET"])
def start_session():
    """Creates a new session ID for a new user."""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())  # Generate a unique session ID
        session["messages"] = []  # Initialize an empty message list
        return jsonify({"message": "New session created!", "session_id": session["session_id"]})
    
    return jsonify({"message": "Session already exists!", "session_id": session["session_id"]})

@app.route("/send", methods=["POST"])
def send_message():
    """Stores user messages in the session."""
    data = request.json  # Get JSON data
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty!"}), 400

    if "session_id" not in session:
        return jsonify({"error": "No active session. Start a session first!"}), 400

    # Store the message in session
    session["messages"].append(user_message)
    
    return jsonify({"message": "Message stored!", "messages": session["messages"]})

@app.route("/history", methods=["GET"])
def get_messages():
    """Returns all stored messages for the current session."""
    if "session_id" not in session:
        return jsonify({"error": "No active session. Start a session first!"}), 400

    return jsonify({"session_id": session["session_id"], "messages": session["messages"]})

if __name__ == "__main__":
    app.run(debug=True)
