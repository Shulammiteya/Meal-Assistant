import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
import utils

load_dotenv()


machine = TocMachine(
    states=["state0", "create_db", "ready", "recommand", "image_choose", "image_wait", "image_watch", "record_watch", "record_choose", "record_wait", "record"],
    transitions=[
        {
            "trigger": "advance",
            "source": "state0",
            "dest": "create_db",
            "conditions": "is_going_to_create_db",
        },
        {
            "trigger": "advance",
            "source": "ready",
            "dest": "recommand",
            "conditions": "is_going_to_recommand",
        },
        {
            "trigger": "advance",
            "source": "ready",
            "dest": "image_choose",
            "conditions": "is_going_to_image_choose",
        },
        {
            "trigger": "advance",
            "source": "image_wait",
            "dest": "image_watch",
            "conditions": "is_going_to_image_watch",
        },
        {
            "trigger": "advance",
            "source": "ready",
            "dest": "record_watch",
            "conditions": "is_going_to_record_watch",
        },
        {
            "trigger": "advance",
            "source": "ready",
            "dest": "record_choose",
            "conditions": "is_going_to_record_choose",
        },
        {
            "trigger": "advance",
            "source": "record_wait",
            "dest": "record",
            "conditions": "is_going_to_record",
        },

        {   "trigger": "go_to_ready",
            "source": ["create_db"],
            "dest": "ready"
        },
        {   "trigger": "go_to_image",
            "source": ["image_choose"],
            "dest": "image_wait"
        },
        {   "trigger": "go_to_record",
            "source": ["record_choose"],
            "dest": "record_wait"
        },
        {   "trigger": "go_back",
            "source": ["recommand", "image_watch", "record_watch", "record"],
            "dest": "ready"
        },
    ],
    initial="state0",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, utils.TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if ( utils.send_guide_flex(event.reply_token) ) == False :
                utils.send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
