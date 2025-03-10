import threading

from api_util import get_api_key
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


class LineBotApp:
    def __init__(self, channel_access_token, channel_secret):
        self.app = Flask(__name__)
        self.line_bot_api = LineBotApi(channel_access_token)
        self.handler = WebhookHandler(channel_secret)
        self.user_ids = set()
        # say you set port as 8000, and you run the dev ngrok tunnel with
        # ngrok 8000, which creates a public ip https://balbla.jp.ngrok.io
        # then you go to line developer console to change the webhook address
        # to https://balbla.jp.ngrok.io/callback, then when you talk to your
        # line bot, it should create the TextMessage event!
        self.app.add_url_rule("/callback", "callback", self.callback, methods=["POST"])

        # webhook trigger callback trigger handler
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            print(event)
            user_id = event.source.user_id
            self.user_ids.add(user_id)
            print(f"User ID: {user_id}")
            message_text = event.message.text
            reply_text = f"Auto-reply: {message_text}"
            self.line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

        self.start_push_timer()

    # the callback trigger by webhook
    def callback(self):
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        try:
            self.handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"

    def send_push_message(self, message_text):
        for user_id in self.user_ids:
            self.line_bot_api.push_message(user_id, TextSendMessage(text=message_text))

    def run(self, host="0.0.0.0", port=8000):
        self.app.run(host=host, port=port)
        self.send_push_message("yooo")

    def start_push_timer(self):
        def push_message_periodically():
            while True:
                for user_id in self.user_ids:
                    self.line_bot_api.push_message(user_id, TextSendMessage(text="yo"))
                threading.Event().wait(5)

        push_thread = threading.Thread(target=push_message_periodically, daemon=True)
        push_thread.start()


if __name__ == "__main__":
    line_bot_app = LineBotApp(get_api_key("LINE_API_ACCESS_TOKEN"), get_api_key("LINE_CHANNEL_SECRET"))
    line_bot_app.run()
