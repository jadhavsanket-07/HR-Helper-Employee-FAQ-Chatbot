import os
import re
import requests
import json
import logging
from flask import Flask, request, jsonify, render_template, redirect
from rapidfuzz import process, fuzz

app = Flask(__name__)

# Path to FAQ JSON file
file_path = r"D:\07-SANKET\Task\data.json"

# Load FAQ dataset
with open(file_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

questions = [item["question"] for item in faq_data]

# Setup logging for questions
logging.basicConfig(
    filename='unknown_questions.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)


@app.route("/")
def home():
    return redirect("/web")


@app.route("/web")
def web_chat():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip() if data else ""
    if not user_message:
        return jsonify({"answer": "Please provide a valid question."})

    best_match = process.extractOne(
        user_message, questions, scorer=fuzz.token_sort_ratio)
    matched_question, score = best_match[0], best_match[1]
    threshold = 60

    if score >= threshold:
        answer = next(item["answer"]
                      for item in faq_data if item["question"] == matched_question)
        return jsonify({"answer": answer})
    else:
        logging.info(f"Unknown question: {user_message}")
        return jsonify({"answer": "Sorry, I don't have an answer for that. We'll review your question soon."})


@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()
    if data and data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    if data and data.get("type") == "event_callback":
        event = data.get("event", {})
        event_type = event.get("type")

        if event_type == "app_mention":
            user = event.get("user")
            text = event.get("text", "")
            channel = event.get("channel")

            cleaned_text = re.sub(r'<@[^>]+>', '', text).strip()

            best_match = process.extractOne(
                cleaned_text, questions, scorer=fuzz.token_sort_ratio)
            matched_question, score = best_match[0], best_match[1]
            threshold = 60

            if score >= threshold:
                answer = next(item["answer"]
                              for item in faq_data if item["question"] == matched_question)
            else:
                answer = "Sorry, I don't have an answer for that. We'll review your question soon."
                logging.info(f"Unknown Slack question: {cleaned_text}")

            bot_token = os.getenv("SLACK_BOT_TOKEN")
            if bot_token:
                headers = {
                    "Authorization": f"Bearer {bot_token}",
                    "Content-Type": "application/json"
                }
                post_message_url = "https://slack.com/api/chat.postMessage"
                payload = {
                    "channel": channel,
                    "text": answer
                }
                resp = requests.post(
                    post_message_url, headers=headers, json=payload)
            else:
                app.logger.error(
                    "SLACK_BOT_TOKEN environment variable not set.")

    return "", 200


@app.route("/slack/oauth_redirect")
def oauth_redirect():
    code = request.args.get("code")
    if not code:
        return "Authorization code not found", 400

    CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")
    # Update if ngrok URL changes
    REDIRECT_URI = "https://2d6bd4ee9a46.ngrok-free.app/slack/oauth_redirect"

    token_url = "https://slack.com/api/oauth.v2.access"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(token_url, data=params)
    token_json = response.json()

    if not token_json.get("ok"):
        error_msg = token_json.get("error", "Unknown error")
        return f"OAuth failed: {error_msg}", 400

    access_token = token_json.get("access_token")
    team_name = token_json.get("team", {}).get("name", "Unknown Team")

    return f"App installation successful for workspace: {team_name}. Access token: {access_token}"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
