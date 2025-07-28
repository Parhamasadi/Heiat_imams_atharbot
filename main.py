from flask import Flask, request
import requests
import datetime

app = Flask(__name__)

RUBIKA_TOKEN = "BBGFB0OBGNABSNBRNNNONGPVZGXEUOMTQMCDLVOVYULIOKZMOUDBRTFEXXIQNCUU"
TELEGRAM_CHANNEL = "https://t.me/s/heiat_imams_athar"

def get_last_telegram_message():
    try:
        response = requests.get(TELEGRAM_CHANNEL)
        if response.ok:
            start = response.text.find('<div class="tgme_widget_message_text')
            if start != -1:
                msg_start = response.text.find(">", start + 35) + 1
                msg_end = response.text.find("</div>", msg_start)
                raw = response.text[msg_start:msg_end]
                text = raw.replace("<br>", "\n").replace("&nbsp;", " ").replace("&quot;", '"').strip()
                return text
        return "پیامی در کانال یافت نشد."
    except:
        return "خطا در دریافت پیام تلگرام."

@app.route('/receiveUpdate', methods=['POST'])
def receive_update():
    data = request.get_json()
    try:
        chat_id = data['update']['chat_id']
        text = data['update']['new_message']['text'].strip().lower()

        if text == "/start" or text == "start":
            welcome = """سلام! 👋✨

به **رباط اطلاع‌رسانی حسینیه فدائیان ائمه اطهار (ع)** خوش آمدید! 🌹

📌 این ربات برای ارائه **اطلاعات برنامه‌های حسینیه، مراسمات، دعاها، سخنرانی‌ها و سایر خدمات فرهنگی** طراحی شده است.

برای مشاهده منوی اصلی، لطفاً یکی از گزینه‌های زیر را انتخاب کنید:

همچنین می‌توانید از دستورات سریع مانند **«برنامه امروز»** استفاده کنید.

✍️ در صورت نیاز به راهنمایی بیشتر، عبارت **«راهنما»** را ارسال کنید.

**یا اباعبدالله الحسین (ع)** ❤️🌙

✉️ **کانال رسمی حسینیه را در سایت ما مشاهده کنید**: [heiat-imams-athar.great-site.net/#contact]

*به محضر امام زمان (عج) و شهدا صلوات!*
🕊️ **اللهم عجل لولیک الفرج**
"""
            send_message(chat_id, "📢 آخرین پیام کانال:\n\n" + last_msg)


        elif text == "برنامه امروز":
            today = datetime.datetime.now().strftime('%A')
            if today == 'Sunday':
                response = """📅 برنامه هفتگی امروز یکشنبه
⏰ زمان : یکشنبه ها از ساعت ۱۸:۳۰ همراه با نماز جماعت

🛐 اقامه نماز جماعت: حاج آقا دشتی
🎤 قرائت زیارت عاشورا: آقای مهدی اسدی
📖 قرائت قرآن کریم: حاج آقا مهدی دشتی
🎤 مداحی: آقای هاشم بشیری

📍 مکان: خیابان کارگر جنوبی، بین میدان پاستور و خیابان آذربایجان، نبش کوچه روشن

اطلاعات بیشتر: http://heiat-imams-athar.great-site.net/#programs
"""
            elif today == 'Thursday':
                response = """📅 برنامه هفتگی امروز پنجشنبه
⏰ زمان : پنجشنبه ها از ساعت ۲۱:۰۰ الی ۱۲ بامداد

🎤 قرائت زیارت عاشورا ، دعای کمیل، دعای توسل به همراه سفره اطعام

📍 مکان: خیابان کارگر جنوبی، بین میدان پاستور و خیابان آذربایجان، نبش کوچه روشن

اطلاعات بیشتر: http://heiat-imams-athar.great-site.net/#programs
"""
            else:
                response = "❌ امروز برنامه‌ای در حسینیه برگزار نمی‌شود."
            send_message(chat_id, response)

        elif text == "راهنما":
            send_message(chat_id, "برای دریافت برنامه‌ها، اخبار و سخنرانی‌ها فقط کلمه «برنامه امروز» یا «شروع» را بفرستید.")
        else:
            send_message(chat_id, "دستور نامشخص است. لطفاً «راهنما» را ارسال کنید.")
    except Exception as e:
        print("خطا:", e)
    return "OK"

def send_message(chat_id, text):
    url = f"https://botapi.rubika.ir/v3/{RUBIKA_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
