
import subprocess

import os
import telebot
import subprocess
from fpdf import FPDF

BOT_TOKEN = '7849254004:AAHneCx6q-Y1gopZPnSxrCWGqr80eWLBEvM'
bot = telebot.TeleBot(BOT_TOKEN)

def generate_pdf(text, filename="result.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(filename)

def run_tool(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True, timeout=60)
        return result
    except subprocess.TimeoutExpired:
        return "Timeout: Took too long."
    except Exception as e:
        return f"Error: {str(e)}"

def search_all(query):
    results = []
    # Sherlock
    results.append("=== Sherlock ===\n")
    results.append(run_tool(f"python3 sherlock/sherlock_project/sherlock.py {query} --print-found"))

    # Holehe (email only)
    if "@" in query:
        results.append("\n=== Holehe ===\n")
        results.append(run_tool(f"python3 holehe/holehe.py {query}"))

        results.append("\n=== EmailRep ===\n")
        results.append(run_tool(f"curl https://emailrep.io/{query}"))

    # PhoneInfoga (number only)
    if query.startswith("+") or query.isdigit():
        results.append("\n=== PhoneInfoga ===\n")
        results.append(run_tool(f"python3 phoneinfoga/phoneinfoga.py scan -n {query}"))

    # theHarvester (email/domain only)
    if "@" in query or "." in query:
        results.append("\n=== theHarvester ===\n")
        results.append(run_tool(f"echo "theHarvester غير مثبت حالياً" -d {query} -b all"))

    # SocialScan (user/email)
    results.append("\n=== SocialScan ===\n")
    results.append(run_tool(f"echo "socialscan غير مثبت حالياً" --username {query} --email {query}"))

    # Skymem (email)
    if "@" in query:
        results.append("\n=== Skymem ===\n")
        results.append(f"https://www.skymem.info/srch?q={query}&ss=srch")

    # Username-Search.org (username)
    if "@" not in query and not query.isdigit():
        results.append("\n=== Username-Search ===\n")
        results.append(f"https://username-search.org/?q={query}")

    return "\n".join(results)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.strip()
    bot.reply_to(message, "جارٍ جمع المعلومات...")

    results = search_all(user_input)
    generate_pdf(results)
    with open("result.pdf", "rb") as f:
        bot.send_document(message.chat.id, f)
    bot.send_message(message.chat.id, "تم الانتهاء.")

bot.infinity_polling()


# استقبال أي رسالة نصية والرد عليها بشكل مبدأي
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.reply_to(message, "تم استلام الرسالة، جاري المعالجة...")

# تشغيل البوت
print("Bot is running...")
bot.infinity_polling()


def run_sherlock(username):
    try:
        result = subprocess.run(['python3', 'sherlock/sherlock.py', username], capture_output=True, text=True, timeout=300)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error running sherlock: {e}"

def run_socialscan(email_or_username):
    try:
        result = subprocess.run(['python3', 'socialscan/socialscan/__main__.py', email_or_username], capture_output=True, text=True, timeout=300)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error running socialscan: {e}"
