
import os
import telebot
import subprocess
from fpdf import FPDF
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '7849254004:AAHneCx6q-Y1gopZPnSxrCWGqr80eWLBEvM'
bot = telebot.TeleBot(BOT_TOKEN)

user_queries = {}
user_results = {}

def run_tool(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True, timeout=60)
        return result
    except subprocess.TimeoutExpired:
        return "Timeout: Took too long."
    except Exception as e:
        return f"Error: {str(e)}"

def generate_pdf(text, filename="result.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, txt=line)
    pdf.output(filename)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text.strip()
    user_queries[message.chat.id] = query

    markup = InlineKeyboardMarkup(row_width=2)

    # Organized tool buttons
    markup.add(InlineKeyboardButton("Sherlock", callback_data="sherlock"),
               InlineKeyboardButton("SocialScan", callback_data="socialscan"))
    markup.add(InlineKeyboardButton("Username-Search", callback_data="usersearch"))

    markup.add(InlineKeyboardButton("Holehe", callback_data="holehe"),
               InlineKeyboardButton("EmailRep", callback_data="emailrep"))
    markup.add(InlineKeyboardButton("Skymem", callback_data="skymem"))

    markup.add(InlineKeyboardButton("PhoneInfoga", callback_data="phoneinfoga"))

    markup.add(InlineKeyboardButton("theHarvester", callback_data="harvester"))

    text = (
        f"أدخلت: {query}

"
        "اختر نوع الأداة حسب نوع البيانات:

"
        "— أدوات البحث عن الاسم (Username):
"
        "Sherlock، SocialScan، Username-Search

"
        "— أدوات البحث عن البريد الإلكتروني:
"
        "Holehe، EmailRep، Skymem

"
        "— أدوات البحث عن رقم الجوال:
"
        "PhoneInfoga

"
        "— أدوات البحث عن الإيميلات والدومينات:
"
        "theHarvester"
    )

    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_tool_selection(call):
    query = user_queries.get(call.message.chat.id)
    tool = call.data
    result = ""

    if not query:
        bot.edit_message_text("لم يتم العثور على استعلام للبحث.", call.message.chat.id, call.message.message_id)
        return

    if tool == "sherlock":
        result = run_tool(f"python3 sherlock/sherlock.py {query} --print-found")
    elif tool == "holehe" and "@" in query:
        result = run_tool(f"python3 holehe/holehe.py {query}")
    elif tool == "emailrep" and "@" in query:
        result = run_tool(f"curl https://emailrep.io/{query}")
    elif tool == "phoneinfoga" and (query.startswith("+") or query.isdigit()):
        result = run_tool(f"python3 phoneinfoga/phoneinfoga.py scan -n {query}")
    elif tool == "harvester" and ("@" in query or "." in query):
        result = run_tool(f"python3 theHarvester/theHarvester.py -d {query} -b all")
    elif tool == "socialscan":
        result = run_tool(f"python3 socialscan/socialscan.py --username {query} --email {query}")
    elif tool == "skymem" and "@" in query:
        result = f"https://www.skymem.info/srch?q={query}&ss=srch"
    elif tool == "usersearch" and "@" not in query and not query.isdigit():
        result = f"https://username-search.org/?q={query}"
    else:
        result = "هذه الأداة لا تدعم نوع البيانات المُدخلة."

    if len(result) > 4000:
        result = result[:4000] + "\n\n(تم تقصير النتيجة...)"

    user_results[call.message.chat.id] = result

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("تحميل النتيجة PDF", callback_data="download_pdf"))

    bot.edit_message_text(f"**نتيجة أداة {tool}:**\n\n{result}", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "download_pdf")
def handle_pdf_download(call):
    result = user_results.get(call.message.chat.id, "لا توجد نتيجة.")
    generate_pdf(result, "result.pdf")
    with open("result.pdf", "rb") as pdf:
        bot.send_document(call.message.chat.id, pdf)
