
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "7981400954:AAGvuTtNbVXNWbfoCQmkvnHaOWvNnfZK0i8"
AUTHORIZED_CHAT_ID = 7293045381

@app.route("/", methods=["POST"])
def receive_message():
    data = request.json
    message = data.get("message", {}).get("text", "")
    chat_id = data.get("message", {}).get("chat", {}).get("id", "")

    # تحقق من الصلاحية
    if chat_id == AUTHORIZED_CHAT_ID:
        if message.startswith("نسخ "):
            code = message.replace("نسخ ", "")
            send_message(chat_id, f"✅ تم نسخ الكود بنجاح:\n\n```
{code}
```")
        else:
            send_message(chat_id, "✅ أرسل لي الكود بعد كلمة 'نسخ'.")
    else:
        send_message(chat_id, "❌ ليس لديك صلاحية للوصول إلى هذه الأوامر.")

    return jsonify({"status": "ok"})

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(port=8000)
